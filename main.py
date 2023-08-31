import streamlit as st
import pandas as pd
import random

# Создание датафрейма 
df = pd.read_csv('data10.csv')

# Функция для стримлинга и печати данных
def stream_data(dataframe, num_rows):
    for _ in range(num_rows):
        random_index = random.randint(0, len(dataframe) - 1)
        row = dataframe.iloc[random_index]
        st.write(f" {row['author']} ---- {row['title']}")

# Основной код Streamlit приложения
def main():
    st.title("Random Data Streaming App")
    
    # num_rows = st.slider("Select number of rows to stream", 1, len(df), 10)
    
    st.write("Streaming data:")
    stream_data(df, 10)

if __name__ == "__main__":
    main()
