/** @jsxImportSource @emotion/react */
import React from "react";
import { css } from "@emotion/react";
import logoSrc from "../../assets/coffee_agntcy.png";

const containerStyle = css`
  height: 10%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #ddd;
  background-color: #ffffff;
  padding: 0;
`;

const imageStyle = css`
  max-height: 60%;
  max-width: 80%;
  object-fit: contain;
`;

const ChatLogo = () => {
    return (
        <div css={containerStyle}>
            <img src={logoSrc} alt="Agency Coffee Logo" css={imageStyle} />
        </div>
    );
};

export default ChatLogo;