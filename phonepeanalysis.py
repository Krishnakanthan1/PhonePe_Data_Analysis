import mysql.connector
import streamlit as st
import matplotlib.pyplot as plt
from tabulate import tabulate
import pandas as pd

st.title("Phonepe Data Analysis")

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Krishna@123",
    database="phonepess"
)

mycursor = mydb.cursor()

# Dropdown for selecting the query
selected_query = st.selectbox("Select a query", ["Which transaction type has the highest count and amount",
                                                 "What is the distribution of users across different brands and states",
                                                 "How does user count varies over different quarters",
                                                 "What are the top districts in terms of transaction count?",
                                                 "How does the distribution of transactions vary across different states",
                                                 "Which districts have the highest number of registered users",
                                                 "How does the number of app opens vary across different districts and quarters",
                                                 "What are the top-performing pincodes in terms of transaction counts and amounts",
                                                 "Which districts have the highest user engagement in terms of counts and amounts",
                                                 "What are the top pincodes in terms of user counts and amounts",
                                                 "How has the performance of top districts changed over different quarters"])

if selected_query == "Which transaction type has the highest count and amount":
    st.header("Which transaction type has the highest count and amount")
    # Query for Transaction Analysis
    query = """
    SELECT Transacion_type , max(Transacion_amount) as amount, max(Transacion_count) as count FROM phonepess.agg_tran
    GROUP BY Transacion_type;
    """
    mycursor.execute(query)

    # Fetch the results
    data = mycursor.fetchall()

    # Display the results in a table using Streamlit
    df = pd.DataFrame(data, columns=[i[0] for i in mycursor.description])
    st.dataframe(df)

    # Plot the line graph using Matplotlib
    st.set_option('deprecation.showPyplotGlobalUse', False)  # Suppress Matplotlib deprecation warning
    fig, ax = plt.subplots()
    ax.plot(df['Transacion_type'], df['amount'], marker='o', linestyle='-')

    # Customize the plot
    plt.xlabel('Transaction Type')
    plt.ylabel('Max Transaction Amount')
    plt.title('Max Transaction Amount by Type')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility

    # Show the plot using Streamlit
    st.pyplot(fig)

elif selected_query == "What is the distribution of users across different brands and states":
    st.header("What is the distribution of users across different brands and states")

    # Query for User Distribution
    query = """
    SELECT brand, sum(count) as total_users FROM Agg_User
    GROUP BY brand;
    """
    mycursor.execute(query)

    # Fetch the results
    data = mycursor.fetchall()

    # Fetch the results into a DataFrame
    df = pd.DataFrame(data, columns=[i[0] for i in mycursor.description])
    st.dataframe(df)

    # Plot a bar chart for the distribution of users across brands
    plt.plot(df['brand'], df['total_users'], linestyle='-')
    plt.xlabel('Brand')
    plt.ylabel('Total Users')
    plt.title('Distribution of Users Across Brands')
    plt.xticks(rotation=45, ha='right')
    st.pyplot()
elif selected_query=="How does user count varies over different quarters":

    st.header("How does user count varies over different quarters")
    querys = """
    SELECT Quarter, SUM(count) AS total_count, avg(percentage) AS max_percentage
    FROM phonepess.agg_user
    GROUP BY Quarter
    order by Quarter asc;
    """

    data = mycursor.execute(querys)

    data = mycursor.fetchall()
    df = pd.DataFrame(data, columns=[i[0] for i in mycursor.description])
    st.dataframe(df)
    plt.plot(df["Quarter"],df["total_count"],linestyle="-")
    plt.xlabel("Quarter")
    plt.ylabel("total_count")
    plt.title("total transaction in every quarter")
    plt.xticks(rotation=45, ha= "right")
    st.pyplot()
# Close the database connectio
elif selected_query=="What are the top districts in terms of transaction count?":
    st.header("What are the top districts in terms of transaction count?")
    querys = """
    SELECT name as district ,max(count) as max_count,max(amount) as max_amount FROM phonepess.map_trans
    group by district
    order by max_count desc
    limit 10;
    """

    data = mycursor.execute(querys)
    data = mycursor.fetchall()
    df = pd.DataFrame(data, columns=[i[0] for i in mycursor.description])
    st.dataframe(df)

    plt.plot(df["district"],df["max_count"])
    plt.xlabel("district")
    plt.ylabel("maximum transaction count")
    plt.title("top 10 districts based on there maximum transaction count")
    plt.xticks(rotation=45 ,ha = "right")
    st.pyplot()

elif selected_query == "How does the distribution of transactions vary across different states":
    st.header("How does the distribution of transactions vary across different states")

    querys = """
    SELECT state, SUM(count) as total_transactions FROM phonepess.map_trans
    GROUP BY state
    order by total_transactions DESC 
    LIMIT 10;
    """

    data = mycursor.execute(querys)
    data = mycursor.fetchall()
    df = pd.DataFrame(data, columns=[i[0] for i in mycursor.description])
    st.dataframe(df)
    plt.plot(df["state"],df["total_transactions"], linestyle ="-")
    plt.xlabel("State")
    plt.ylabel("total_transaction")
    plt.title("Top 10 state based on total transaction count")
    plt.xticks(rotation=45 , ha ="right")
    st.pyplot()
elif selected_query=="Which districts have the highest number of registered users":
    st.header("Which districts have the highest number of registered users")
    querys = """
    SELECT districts, sum(registered_users) as total_users FROM phonepess.map_user
    group by districts
    order by total_users DESC
    limit 10;
    """
    data=mycursor.execute(querys)
    data=mycursor.fetchall()
    df=pd.DataFrame(data, columns=[i[0] for i in mycursor.description] )
    st.dataframe(df)
    plt.plot(df["districts"],df["total_users"],linestyle="-")
    plt.xlabel("districts")
    plt.ylabel("total_users")
    plt.title("top 10 districts based on users")
    plt.xticks(rotation=45 , ha="right")
    st.pyplot()
elif selected_query=="How does the number of app opens vary across different districts and quarters":
    st.header("How does the number of app opens vary across different districts and quarters")
    querys = """
    SELECT Quarter, districts, sum(app_opens) as total_opens FROM phonepess.map_user
    Group by districts, Quarter
    order by total_opens DESC
    Limit 10;
    """
    data=mycursor.execute(querys)
    data=mycursor.fetchall()
    df=pd.DataFrame(data, columns=[i[0] for i in mycursor.description])
    st.dataframe(df)
    df['total_opens'] = pd.to_numeric(df['total_opens'])
    df.set_index(["districts", "Quarter"]).plot(kind='bar', stacked=True, figsize=(12, 6))
    plt.xlabel("district and quater")
    plt.ylabel("total_opens")
    plt.title("app opens vary across different districts and quarters")
    plt.legend(title='Metric')
    st.pyplot()

elif selected_query=="What are the top-performing pincodes in terms of transaction counts and amounts":
    st.header("What are the top-performing pincodes in terms of transaction counts and amounts")
    query = """
    SELECT state, pincode, pi_amount
    FROM phonepess.top_tranpin
    ORDER BY pi_amount DESC
    LIMIT 10 ;
    """
    data=mycursor.execute(query)
    data=mycursor.fetchall()
    df=pd.DataFrame(data, columns=[i[0] for i in mycursor.description])
    st.dataframe(df)
    df.set_index(['state', 'pincode']).plot(kind='bar', stacked=True, figsize=(12, 6))
    plt.xlabel('State and Pincode')
    plt.ylabel('Value')
    plt.title('Top Pin Codes with Highest Transaction Amounts and Counts')
    plt.legend(title='Metric')
    st.pyplot()
elif selected_query=="Which districts have the highest user engagement in terms of counts and amounts":
    st.header("Which districts have the highest user engagement in terms of counts and amounts")
    query = """
    SELECT state, district , max(registeredUsers) as max_registereduser FROM phonepess.top_usdist
    group by state, district
    order by max_registereduser desc
    limit 10;
    """
    data=mycursor.execute(query)
    data=mycursor.fetchall()
    df=pd.DataFrame(data, columns=[i[0] for i in mycursor.description])
    st.dataframe(df)
    df.set_index(["state","district"]).plot(kind='bar', stacked=True, figsize=(12, 6))
    plt.xlabel("state and there districts")
    plt.ylabel("max_registeredusers")
    plt.title("bbjbjb")
    plt.legend(title='Metric')
    st.pyplot()
elif selected_query=="What are the top pincodes in terms of user counts and amounts":
    st.header("What are the top pincodes in terms of user counts and amounts")
    query = """
    SELECT state,Year, max(registeredUsers) as max_users FROM phonepess.top_uspin
    group by state,Year
    Order by max_users Desc
    Limit 10;
    """
    data=mycursor.execute(query)
    data=mycursor.fetchall()
    df=pd.DataFrame(data,columns=[i[0]for i in mycursor.description])
    st.dataframe(df)
    df.set_index(['state', 'Year']).plot(kind='bar', stacked=True, figsize=(12, 6))
    plt.xlabel('State and year')
    plt.ylabel('max_user')
    plt.title('Top Pin Codes with Highest Transaction Amounts and Counts')
    plt.legend(title='Metric')
    st.pyplot()
elif selected_query=="How has the performance of top districts changed over different quarters":
    st.header("How has the performance of top districts changed over different quarters")
    query = """
    SELECT Quarter, district, sum(di_count) as total_count FROM phonepess.top_trandis
    Group by Quarter, district
    Order by total_count DESC
    Limit 10;
    """
    data=mycursor.execute(query)
    data=mycursor.fetchall()
    df=pd.DataFrame(data,columns=[i[0] for i in mycursor.description])
    st.dataframe(df)
    #df['total_amount'] = pd.to_numeric(df['total_amount'])
    df['total_count'] = pd.to_numeric(df['total_count'])
    df.set_index(['Quarter', 'district']).plot(kind='bar', figsize=(12, 6))
    plt.xlabel('Quarter and district')
    plt.ylabel('Value')
    plt.title('Top Pin Codes with Highest Transaction Amounts and Counts')
    plt.legend(title='Metric')
    st.pyplot()
mydb.close()



