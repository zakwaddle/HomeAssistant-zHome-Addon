import { createGlobalStyle } from 'styled-components'

const GlobalStyle = createGlobalStyle`
  html, body {
    margin: 0;
    padding: 0;
    overflow-x: hidden;

  }
  
  h1, h2, h3, h4, h5, h6, p {
    margin: 0;
    padding: 0;
  }
  
  body {
    font-size: 12px;
    color: #e1e1e1;
    background-color: #111111;
    @media (max-width: 429px) {
      font-size: 14px;
    }
  }

`

export default GlobalStyle;