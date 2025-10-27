def chatbot_ui(compact: bool = False):
    """Displays Ella chat UI. Compact=True makes it fit smaller popups."""

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Adjust placeholder based on mode
    placeholder = (
        "Ask Ella anything..." if compact
        else "Ask Ella anything about nutrition, meals, or food choices..."
    )

    # User input (with unique key per context)
    if prompt := st.chat_input(
        placeholder,
        key=f"chat_input_{st.session_state.get('chat_context', 'default')}"
    ):
        # Append user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            response = generate_response(prompt)
            st.markdown(response)

        # Save assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})

