import React from "react";
import GlobalStyle from "../styles/GlobalStyles";
import styled from 'styled-components';
import LogSection from "./Logs";
import ControlSection from "./Controls/ControlSection";
import useSSE from "../hooks/useSSE";
import Menu from "./Controls/Menu/Menu";
import {useSelector} from "react-redux";


const AppContainer = styled.div`
  height: 100%;
  width: 100%;
  padding: .5em;
  font-family: monospace;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`

export default function App() {
    useSSE();
    const menuSelection = useSelector(state => state['globalState']['menuSelection'])
    return (
        <AppContainer>
            <GlobalStyle/>
            <Menu/>
            {menuSelection !== "Logs" && <ControlSection/>}
            {menuSelection === "Logs" && <LogSection/>}
        </AppContainer>
    );
};