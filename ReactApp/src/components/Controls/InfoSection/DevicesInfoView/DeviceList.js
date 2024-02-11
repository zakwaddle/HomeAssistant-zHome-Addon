import React, {useState} from "react";
import styled from "styled-components";
import useApi from "../../../../hooks/useApi";
import {useDispatch, useSelector} from "react-redux";
import {globalStateActions} from "../../../../store/globalStateSlice";
import {PropStack} from "../../../UI/Property";


const DeviceListContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  @media (min-width: 700px) {
    min-height: 10em;
    //transition: height 500ms ease-in-out 500ms;
    ${props => props['hasSelected'] ?
            'transition: height 500ms ease-in-out 500ms'
            :
            'transition: height 200ms ease-in-out 100ms'}
  }
`

const DeviceContainer = styled.div`
  background-color: ${props => props['selected'] ? 'grey' : undefined};
  color: ${props => props['selected'] ? 'white' : undefined};
  display: flex;
  justify-content: space-between;
  border: 1px solid ${props => props['selected'] ? 'white' : 'black'};
  border-radius: 1em;
  padding: .25em 2em .25em 2em;
  transition: all 0.2s ease-in-out; // Add transition effect here
  transition-delay: 50ms;
  //transition: background-color 0.2s ease-in-out 0.1s, color 0.3s ease-in-out 0.1s, border 0.3s ease-in-out 0.1s;

  margin: .25em;
  align-items: center;
  cursor: pointer;
  @media (max-width: 700px) {
    ${props => props['hide'] ?
            'transition: height 800ms ease-out, opacity 200ms ease-out, padding 100ms ease-out, margin 100ms ease-out; cursor: none;'
            :
            'transition: height 500ms ease-in 300ms, opacity 500ms ease-in;'}
    border: ${props => props['hide'] ? '0' : `1px solid ${props['selected'] ? 'white' : 'black'}`};
    //transition-delay: 0ms;
    padding: ${props => props['hide'] ? '0' : '.25em 2em .25em 2em'};
    margin: ${props => props['hide'] ? '0' : '.25em'};
    opacity: ${props => props['hide'] ? '0' : '1'}; // hide the element using opacity
    height: ${props => props['hide'] ? '0' : 'content-box'}; // hide the element by reducing its height
  }
`
const Button = styled.button`
  font-family: monospace;
  font-size: inherit;
  background-color: inherit;
  border-radius: .3em;
  border-width: 1px;
`

const Device = ({deviceData}) => {
    const dispatch = useDispatch()
    const selectedDevice = useSelector(state => state['globalState']['selectedDevice'])
    const isSelected = selectedDevice === deviceData
    const noSelection = selectedDevice === null
    const handleClick = () => {
        if (isSelected) {
            dispatch(globalStateActions.updateSelectedDevice(null))
        } else {
            dispatch(globalStateActions.updateSelectedDevice(deviceData))

        }
    }
    const platform = (deviceData.platform === 'rp2' ? 'PicoW' : 'ESP32')
    return (
        <DeviceContainer selected={isSelected}
                         hide={!isSelected && !noSelection}
                         onClick={handleClick}>
            <PropStack label={'Name'}>{deviceData.display_name}</PropStack>
            <p><b>{platform}</b></p>
        </DeviceContainer>
    )
}
export const DeviceList = ({selectedDevice, setSelectedDevice}) => {
    const devices = useSelector(state => state['globalState']['devices'])
    // console.log(devices)
    return (
        <DeviceListContainer hasSelected={selectedDevice !== null}>
            {devices.map(device => <Device key={device.id}
                                           deviceData={device}
                                           selected={selectedDevice}
                                           setSelected={setSelectedDevice}/>)}
        </DeviceListContainer>
    )
}


const DeviceSetupBox = styled.div`
  width: 95%;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease-in-out; // Add transition effect here

`
const DeviceSetupRow = styled.div`
  width: 95%;
  display: flex;
  justify-content: space-evenly;
`
export const DeviceSetup = ({device, setShowSetup}) => {
    const [newName, setNewName] = useState("")

    const {updateDeviceName} = useApi()

    const handleCancel = () => setShowSetup(false)
    const handleSetup = () => {
        updateDeviceName(device.id, newName).then(setShowSetup(false))
    }
    return (
        <DeviceSetupBox>
            <DeviceSetupRow>
                {device.platform}
                {device.id}
            </DeviceSetupRow>
            <DeviceSetupRow>
                Display Name
                <input value={newName} onChange={event => setNewName(event.target.value)}/>
            </DeviceSetupRow>
            <DeviceSetupRow>
                <Button onClick={handleCancel}>Cancel</Button>
                <Button onClick={handleSetup}>Save</Button>
            </DeviceSetupRow>
        </DeviceSetupBox>
    )
}

