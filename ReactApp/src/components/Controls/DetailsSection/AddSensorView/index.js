import React, {useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {globalStateActions} from "../../../../store/globalStateSlice";
import styled from "styled-components";
import AddMotionSensorForm from "./AddMotionSensorForm";
import AddWeatherSensorForm from "./AddWeatherSensorForm";
import AddLEDDimmerForm from "./AddLEDDimmerForm";
import AddFanForm from "./AddFanForm";
import AddButtonForm from "./AddButtonForm";
import {Button} from "../../../../styles/SectionStyles";

const AddSensorContainer = styled.div`
  width: 100%;
  height: 100%;
  //background-color: burlywood;
  display: flex;
  flex-direction: column;
  justify-content: center;
`
const Wrapper = ({children}) => {
    return [...children]
}
const AddSensorView = () => {
    const dispatch = useDispatch()
    const selectedDevice = useSelector(state => state['globalState']['selectedDevice'])
    const config = selectedDevice.config

    const [sensorType, setSensorType] = useState('');

    const setDetailsView = () => dispatch(globalStateActions.updateDetailsSectionView('main'))
    const updateDevice = () => dispatch(globalStateActions.updateShouldUpdateDevices(true))
    const sensorForms = {
        "": (
            <Wrapper>
                <Button onClick={() => setSensorType('motion')}>Motion Sensor</Button>
                <Button onClick={() => setSensorType('weather')}>Weather Sensor</Button>
                <Button onClick={() => setSensorType('led')}>LED Dimmer</Button>
                <Button onClick={() => setSensorType('fan')}>Fan</Button>
                <Button onClick={() => setSensorType('button')}>Button</Button>
                <Button onClick={() => setDetailsView()}>Cancel</Button>
            </Wrapper>
        ),
        "motion": <AddMotionSensorForm updateDevice={updateDevice}
                                       deviceName={selectedDevice.display_name}
                                       deviceConfigId={config.id}
                                       handleCancel={setDetailsView}/>,
        "weather": <AddWeatherSensorForm updateDevice={updateDevice}
                                         deviceName={selectedDevice.display_name}
                                         deviceConfigId={config.id}
                                         handleCancel={setDetailsView}/>,
        "led": <AddLEDDimmerForm updateDevice={updateDevice}
                                 deviceName={selectedDevice.display_name}
                                 deviceConfigId={config.id}
                                 handleCancel={setDetailsView}/>,
        "fan": <AddFanForm updateDevice={updateDevice}
                           deviceName={selectedDevice.display_name}
                           deviceConfigId={config.id}
                           handleCancel={setDetailsView}/>,
        "button": <AddButtonForm updateDevice={updateDevice}
                           deviceName={selectedDevice.display_name}
                           deviceConfigId={config.id}
                           handleCancel={setDetailsView}/>,
    }
    return (
        <AddSensorContainer>
            {sensorForms[sensorType]}
        </AddSensorContainer>

    );
};

export default AddSensorView