import React from "react";

const Message = ({ role, content }) => {
  const isUser = role === "User";

  return (
    <div
      style={{
        textAlign: isUser ? "right" : "left",
        margin: "10px 0",
      }}
    >
      <div
        style={{
          display: "inline-block",
          padding: "10px",
          borderRadius: "10px",
          background: isUser ? "#007bff" : "#f1f1f1",
          color: isUser ? "white" : "black",
          maxWidth: "70%",
        }}
      >
        {content}
      </div>
    </div>
  );
};

export default Message;
