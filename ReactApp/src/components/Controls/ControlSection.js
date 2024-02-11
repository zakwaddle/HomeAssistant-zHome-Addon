import React from "react";
import styled from "styled-components";
// import Menu from "./Menu/Menu";
import useConnections from "../../hooks/useConnections";
import DetailSection from "./DetailsSection";
import InfoSection from "./InfoSection";
import useDevices from "../../hooks/useDevices";
import {useSelector} from "react-redux";

const ControlSectionBox = styled.div`
  width: 100%;
  display: flex;
  justify-content: space-around;
  margin: 1em 1em 0 1em;

  @media (max-width: 700px) {
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
`

const InfoWindow = styled.div`
  width: 30%;
  padding: 1em;

  display: flex;
  flex-direction: column;
  //justify-content: center;

  background-color: white;
  border: 1px solid darkgrey;
  border-radius: 1em;


  @media (max-width: 700px) {
    flex-direction: column;
    width: 95%;
    ${props => props['hasSelected'] ?
            'transition: height 500ms ease-in-out 500ms'
            :
            'transition: height 200ms ease-in-out 100ms'}
  }    //height: content-box;
  }
`

const DetailsWindow = styled.div`
  width: 50%;
  padding: 1em;

  display: flex;
  flex-direction: column;

  background-color: white;
  border: 1px solid darkgrey;
  border-radius: 1em;

  @media (max-width: 700px) {


    opacity: ${props => !props['visible'] ? '0' : '1'}; // hide the element using opacity
    height: ${props => !props['visible'] ? '0' : 'auto'}; // hide the element by reducing its height
    transition: all 1s ease-in-out; // Add transition effect
    transition-delay: 250ms;
    width: 95%;
    align-items: center;
      // display: ${props => props['visible'] ? 'flex' : 'none'};
  }

`
const ControlSection = () => {
    useConnections()
    useDevices()
    const selectedDevice = useSelector(state => state['globalState']['selectedDevice'])
    const menuSelection = useSelector(state => state['globalState']['menuSelection'])
    const isVisible = menuSelection === 'Devices' && !!selectedDevice

    return (
        <ControlSectionBox>
            {/*<Menu/>*/}
            <InfoWindow hasSelected={selectedDevice !== null}>
                <InfoSection/>
            </InfoWindow>
            <DetailsWindow visible={isVisible}>
                <DetailSection/>
            </DetailsWindow>
        </ControlSectionBox>
    )
}

export default ControlSection;