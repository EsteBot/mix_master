import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

st.set_page_config(layout="wide")

# CSS to center the elements
st.markdown(
    """
    <style>
    .center {
        display: flex;
        justify-content: center;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Centering the headers
st.markdown("<h2 class='center' style='color:rgb(80, 200, 120);'>An EsteStyle Streamlit Page<br>Where Python Wiz Meets Data Viz!</h2>", unsafe_allow_html=True)
st.markdown("<h2 class='center'></h2>", unsafe_allow_html=True)

st.markdown("<img src='https://1drv.ms/i/s!ArWyPNkF5S-foZspwsary83MhqEWiA?embed=1&width=307&height=307' width='300' style='display: block; margin: 0 auto;'>" , unsafe_allow_html=True)

st.markdown("<h2 class='center'></h2>", unsafe_allow_html=True)

st.markdown("<h2 class='center' style='color: rgb(80, 200, 120);'>RatioMaster: Flexible Mixing Simplified</h2>", unsafe_allow_html=True)

st.markdown("<h2 class='center'></h2>", unsafe_allow_html=True)

st.markdown("<h3 class='center' style='color: gold;'>🐱Concept originated at the University of Colorado Denver 🐾</h3>" , unsafe_allow_html=True)
st.markdown("<h3 class='center' style='color: gold;'>🧪In the Laboratory for Behavioral Neuroscience🧠</h3>", unsafe_allow_html=True)
st.markdown("<h3 class='center' style='color: rgb(80, 200, 120);'>🤖By Esteban C Loetz 💾</h3>" , unsafe_allow_html=True)

st.markdown("<h1 class='center'></h1>", unsafe_allow_html=True)

# Create Streamlit app
col_list = st.columns([1, 2, 2, 1])

# Initialize session state for the number of assets and tickers list
if "num_of_sols" not in st.session_state:
    st.session_state.num_of_sols = 1

if "num_of_mL" not in st.session_state:
    st.session_state.num_of_mils = 1

if "IDs" not in st.session_state:
    st.session_state.IDs = []

if "ratios" not in st.session_state:
    st.session_state.ratios = []

with col_list[1]:
    st.title("End Volume")
    # Store the number of mL in session state
    st.session_state.num_of_mils = st.number_input("Enter end volume of the solution to be created (mL)", min_value=0.01, max_value=10000.0, step=0.01)

with col_list[2]:
    st.title("Total Solutions")
    # Store the number of solutions in session state
    st.session_state.num_of_sols = st.number_input("Enter number of solutions to be mixed", min_value=1, max_value=100)

with col_list[2]:
    # Space holder to match next inputs alignment
    st.markdown("<h1 class='center'></h1>", unsafe_allow_html=True)
    st.markdown("<h1 class='center'></h1>", unsafe_allow_html=True)

with col_list[1]:
    st.write("")
    if st.button("Create Solution IDs & Their Ratio Fields ⚗️"):
        # Reset solution list in session state based on the updated number of solutions
        st.session_state.IDs = ["" for _ in range(st.session_state.num_of_sols)]
        st.session_state.ratios = ["" for _ in range(st.session_state.num_of_sols)]

# If solutions were created, display solution input fields
if st.session_state.ratios:
    with col_list[1]:
        st.title("Solution IDs")
        st.write("e.g., Solution 1")
        for i in range(st.session_state.num_of_sols):
            # Use session state to keep values for each solution input
            st.session_state.IDs[i] = st.text_input(f"Enter Solution ID #{i + 1}", st.session_state.IDs[i], key=f"ID_{i}")

    with col_list[2]:
        st.title("Number of Parts:")
        st.write("e.g., 1, as in 1 part of the whole")
        for i in range(st.session_state.num_of_sols):
            # Use session state to keep values for each solution input
            st.session_state.ratios[i] = st.text_input(f"Enter Solution Part", st.session_state.ratios[i], key=f"Ratio_{i}")

    with col_list[1]:
        st.write("")
        analysis_button = st.button("Perform Ratio Volume Calcs 📟")

    with col_list[2]:
        st.markdown("<h1 class='center'></h1>", unsafe_allow_html=True)
        st.markdown("<h1 class='center'></h1>", unsafe_allow_html=True)
    
    
    if analysis_button:
        try:
            # Calculate total parts
            total_parts = sum([float(ratio) for ratio in st.session_state.ratios if ratio.strip()])
            solution_volumes = [
                {
                    "Solution ID": st.session_state.IDs[i],
                    "Parts": float(st.session_state.ratios[i]),
                    "Volume (mL)": round(
                        (float(st.session_state.ratios[i]) / total_parts) * st.session_state.num_of_mils, 2
                    )
                }
                for i in range(st.session_state.num_of_sols)
                if st.session_state.ratios[i].strip()
            ]

            # Create the DataFrame
            df = pd.DataFrame(solution_volumes)

            # **Dynamic Colors**
            num_solutions = st.session_state.num_of_sols  # Get number of solutions
            cmap = cm.get_cmap("tab20", num_solutions * 2)  # Generate a larger colormap to have more options
            colors = [cmap(i) for i in range(num_solutions * 2) if not (cmap(i)[0] == 0.6 and cmap(i)[1] == 0.4 and cmap(i)[2] == 0.2)]  # Filter out 'brown'

            # Ensure we have enough colors after filtering
            colors = colors[:num_solutions]

            # Set a consistent figure size
            consistent_figsize = (6, 6)  # Width, Height in inches
            title_fontsize = 26
            label_fontsize = 16
            legend_fontsize = 14

            # **Pie Chart**
            # Extract labels and sizes
            labels = df["Solution ID"]
            sizes = df["Volume (mL)"]

            # Create pie chart
            fig, ax = plt.subplots(figsize=consistent_figsize)
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, textprops={'fontsize': label_fontsize}, wedgeprops={'edgecolor': 'black'})
            ax.axis('equal')  # Equal aspect ratio to make the pie circular
            ax.set_title("Percent Volume by Solution", fontsize=title_fontsize, pad=20)

            with col_list[1]:
                # Display the pie chart
                plt.tight_layout()
                st.pyplot(fig)

            ## **Stacked Bar Chart**
            # Prepare the data
            x = np.array(["Final Volume"])  # Single category for stacking
            y_values = df["Volume (mL)"]
            bottom = 0  # Keep track of the "stack"

            fig, ax = plt.subplots(figsize=consistent_figsize)
            for i, (label, value, color) in enumerate(zip(labels, y_values, colors)):
                # Add bar
                bar = ax.bar(x, value, label=label, bottom=bottom, color=color, edgecolor='black')
                # Add text annotation in the middle of the stack
                ax.text(
                    x=bar[0].get_x() + bar[0].get_width() / 2,  # Center horizontally
                    y=bottom + value / 2,  # Center vertically
                    s=f"{value:.2f} mL",  # Format text
                    ha="center", va="center", fontsize=label_fontsize, color="black"  # Center alignment & style
                )
                bottom += value  # Update the bottom for the next stack

            # Add title, legend, and labels
            ax.set_title("Volume Contributions", fontsize=title_fontsize, pad=20)
            ax.set_ylabel("Volume (mL)", fontsize=label_fontsize)
            ax.set_xticklabels(["Final Volumes"], fontsize=label_fontsize)
            ax.legend(title="Solutions", fontsize=legend_fontsize, title_fontsize=legend_fontsize, bbox_to_anchor=(1.05, 1), loc='upper left')  # Legend outside plot
            # Increase font size of y-axis label numbers
            ax.tick_params(axis='y', labelsize=label_fontsize)

            # Remove top and right spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            with col_list[2]:
                # Display the stacked bar chart
                plt.tight_layout()
                st.pyplot(fig)

            with col_list[1]:
                # **Text Output with Matching Colors**
                st.title("Solution Volumes")
                for i, solution in enumerate(solution_volumes):
                    # Convert RGBA to HEX
                    color_hex = "#{:02x}{:02x}{:02x}".format(
                        int(colors[i][0] * 255), int(colors[i][1] * 255), int(colors[i][2] * 255)
                    )
                    
                    # Wrap the entire text in a styled <span>
                    st.markdown(
                        f"<span style='color:{color_hex}; font-weight:bold;'>{solution['Solution ID']}: "
                        f"{solution['Volume (mL)']} mL ({solution['Parts']} parts)</span>",
                        unsafe_allow_html=True
                    )

        except ValueError:
            st.error("Please ensure that there are more than one number of solutions & all entered ratios are numeric values.")
