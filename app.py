import streamlit as st
from movie_details import fetch_movie_details, display_movie_details
import pandas as pd
import json

ALLOWED_EXTENSIONS = {'txt', 'csv'}  # Add the allowed file extensions here

def main():
    st.title("Find This Film")
    st.header("Get Movie Details")
    film_name = st.text_input("Enter Film Name:")
    year_of_release = st.text_input("Enter Year of Release:")
    st.header("Upload a File")
    uploaded_file = st.file_uploader("Choose a file", type=ALLOWED_EXTENSIONS)

    if st.button("Get Details"):
        if uploaded_file is not None:
            # Process the uploaded file
            file_content = uploaded_file.read().decode('utf-8').split('\n')
            results = []
            for line in file_content:
                parts = [part.replace('"', '').strip() for part in line.split(',')]
                if len(parts) == 2:
                    film, year = parts
                    result = fetch_movie_details(film, year)
                    results.append(result)

            results = [result if 'error' not in result else {'error': result['error']} for result in results]

            st.header("Results")
            for result in results:
                display_movie_details(result)
            
            # Add a button to download the results as JSON
            download_button = st.download_button(
                label="Download results as JSON",
                data=json.dumps(results, indent=2),
                file_name="movie_details_results.json",
                key="download_json_button"
            )
            
            # Convert the results to a DataFrame
            df_results = pd.DataFrame(results)

            # Add a button to download the results as CSV
            download_csv_button = st.download_button(
                label="Download results as CSV",
                data=df_results.to_csv(index=False),
                file_name="movie_details_results.csv",
                key="download_csv_button"
            )
        else:
            result = fetch_movie_details(film_name, year_of_release)

            if 'error' in result:
                st.error(result['error'])
            else:
                display_movie_details(result)
                
                # Add a button to download the result as JSON
                download_button = st.download_button(
                    label="Download results as JSON",
                    data=json.dumps(result, indent=2),
                    file_name="movie_details_results.json",
                    key="download_json_button"
                )
                
                # Convert the results to a DataFrame
                df_result = pd.DataFrame(result)

                # Add a button to download the results as CSV
                download_csv_button = st.download_button(
                    label="Download results as CSV",
                    data=df_result.to_csv(index=False),
                    file_name="movie_details_results.csv",
                    key="download_csv_button"
                )

if __name__ == "__main__":
    main()
