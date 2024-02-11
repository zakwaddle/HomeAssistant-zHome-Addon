import React from "react";
import {useDispatch, useSelector} from "react-redux";
import {Button} from "../../../styles/SectionStyles";
import {globalStateActions} from "../../../store/globalStateSlice";
import styled from "styled-components";


const MenuButton = styled.button`
  font-family: monospace;
  //font-size: inherit;
  width: 9em;
  background-color: ${props => props['selected'] ? 'grey' : 'inherit'};
  border-color: ${props => props['selected'] ? 'white' : 'grey'};
  color: ${props => props['selected'] ? 'white' : 'grey'};
  padding: .25em;
  margin: .5em;
  border-radius: .3em;
  border-width: 1px;
`
const MenuItem = ({children}) => {
    const dispatch = useDispatch()
    const menuSelection = useSelector(state => state['globalState']['menuSelection'])
    const handleSelection = () => {
        dispatch(globalStateActions.updateMenuSelection(children))
    }
    return (
        <MenuButton selected={menuSelection === children} onClick={handleSelection}>
            {children}
        </MenuButton>
    )
}

const MenuBox = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 100%;
  //height: 100%;
  //width: 10em;
  //flex-direction: column;
  //
  //@media (max-width: 700px) {
  //  flex-direction: row;
  //  justify-content: center;
  //  width: 100%;
  //}
`
const Menu = () => {

    return (
        <MenuBox>
            <MenuItem>Devices</MenuItem>
            <MenuItem>Connections</MenuItem>
            <MenuItem>Logs</MenuItem>
        </MenuBox>
    )
}

export default Menu;