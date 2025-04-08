const jsVariables = document.getElementById('js-variables');
const getChatsUrl = jsVariables.dataset.getChatsUrl;
const postChatUrl = jsVariables.dataset.postChatUrl;
const recipient = jsVariables.dataset.recipient; // recipient id as a string
const csrfToken = getCookie("csrftoken");

const getChatsUrlWithRecipient = getChatsUrl + '?recipient=' + encodeURIComponent(recipient);


    function loadChatboxMessages(){
          fetch(getChatsUrlWithRecipient)
              .then(response => response.json())
              .then(data => {
                  const messagesDiv = document.getElementById('chat-messages');
                  messagesDiv.innerHTML = "";  // clear current messages
                  data.messages.forEach(msg => {
                    const div = document.createElement('div');
                    div.innerHTML = "<strong>" + msg.sender + ":</strong> " + msg.message + " <em>(" + msg.timestamp + ")</em>";
                    messagesDiv.appendChild(div);
                  });
              });
      }
      // Poll every 15 seconds.
      setInterval(loadChatboxMessages, 15000);
      // Also load messages on page load.
      loadChatboxMessages();


    // Post a chat message
const chatForm = document.getElementById('chat-form');
    if (chatForm) {
          chatForm.onsubmit = function(e) {
              e.preventDefault();
              const messageInput = document.getElementById("chat-input");
              const message = messageInput.value;
              fetch(postChatUrl, {
                  method: "POST",
                  headers: {
                      "Content-Type": "application/x-www-form-urlencoded",
                      "X-CSRFToken": csrfToken
                  },
                  body: new URLSearchParams({
                      "message": message,
                      "recipient": recipient
                  })
              })
              .then(response => response.json())
              .then(data => {
                  if(data.status === 'ok'){
                      messageInput.value = '';
                      loadChatboxMessages(); // Refresh the messages
                  }
              });
              return false;
          };
      }

      // Function to get CSRF token from the cookie, as django doesn't parse inside external javascript.
      function getCookie(name) {
          let cookieValue = null;
          if (document.cookie && document.cookie !== "") {
              const cookies = document.cookie.split(";");
              for (let i = 0; i < cookies.length; i++) {
                  const cookie = cookies[i].trim();
                  if (cookie.substring(0, name.length + 1) === (name + "=")) {
                      cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                      break;
                  }
              }
          }
          return cookieValue;
      }