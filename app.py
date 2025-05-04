import streamlit as st

# Required for Railway's health check system
def main():
    print("✅ Streamlit app entrypoint reached")  # Now visible in logs
    st.title("Hello from Team Ray!")
    
    # Essential root endpoint response
    st.write("OK")  # Simple 200 response for health checks

if __name__ == "__main__":
    main()  # Ensures proper execution context