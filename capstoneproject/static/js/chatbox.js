const jsVariables = document.getElementById('js-variables');
const getChatsUrl = jsVariables.dataset.getChatsUrl;
const postChatUrl = jsVariables.dataset.postChatUrl;
const recipient = Number(jsVariables.dataset.recipient); // recipient id as a string
const viewer = Number(jsVariables.dataset.viewer);
const csrfToken = getCookie("csrftoken");

const getChatsUrlWithRecipient = getChatsUrl + '?recipient=' + encodeURIComponent(recipient);


    function loadChatboxMessages(){
          fetch(getChatsUrlWithRecipient)
              .then(response => response.json())
              .then(data => {
                  const messagesDiv = document.getElementById('chat-messages');
                  messagesDiv.innerHTML = "";  // clear current messages
                  data.messages
                    .filter(msg => {
                    if (viewer === recipient) return true;
                    if (msg.is_announcement) return true;
                    if (!msg.is_admin && !msg.is_system) return true;
                    if (msg.sender_id === viewer) return true;
                    return false;
        })
                    .forEach(msg => {
                        const div = document.createElement("div");
                        div.classList.add("chat-message");

                        if (msg.is_admin) {
                            div.classList.add("admin-message");
                        }
                        if (msg.is_system) {
                            div.classList.add("system-message");
                        }
                        if (msg.is_announcement) {
                            div.classList.add("announcement-message");
                        }
                        let displayName = msg.sender;
                        if (msg.is_admin)  displayName += " (Staff)";

                    div.innerHTML = "<strong>" + displayName + ":</strong> " + msg.message + " <em>(" + msg.timestamp + ")</em>";
                    messagesDiv.appendChild(div);
                  });
              });

      }
      // Poll every 5 minutes to stop console spam
      setInterval(loadChatboxMessages, 300000);
      // Also load messages on page load.
      loadChatboxMessages();


    // Post a chat message
const chatForm = document.getElementById('chat-form');
    if (chatForm) {
          chatForm.onsubmit = function(e) {
              e.preventDefault();
              const messageInput = document.getElementById("chat-input");
              const message = messageInput.value;
              const asStaff = document.getElementById("as_staff")?.checked ? "1" : "";
              fetch(postChatUrl, {
                  method: "POST",
                  headers: {
                      "Content-Type": "application/x-www-form-urlencoded",
                      "X-CSRFToken": csrfToken
                  },
                  body: new URLSearchParams({
                      "message": message,
                      "recipient": recipient,
                       as_staff: asStaff
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