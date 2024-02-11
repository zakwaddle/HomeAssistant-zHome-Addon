import React, {useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {globalStateActions} from "../../../../store/globalStateSlice";
import styled from "styled-components";
import AddMotionSensorForm from "./AddMotionSensorForm";
import AddWeatherSensorForm from "./AddWeatherSensorForm";
import AddLEDDimmerForm from "./AddLEDDimmerForm";

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

    const [sensorType, setSensorType] = useState('motion');

    const handleChange = (event) => setSensorType(event.target.value)
    const setDetailsView = () => dispatch(globalStateActions.updateDetailsSectionView('main'))
    const updateDevice = () => dispatch(globalStateActions.updateShouldUpdateDevices(true))
    const sensorForms = {
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
    }
    return (
        <AddSensorContainer>
            <div>
                <select onChange={handleChange}>
                    <option value={'motion'}>Motion Sensor</option>
                    <option value={'weather'}>Weather Sensor</option>
                    <option value={'led'}>LED Dimmer</option>
                </select>
            </div>

            {sensorForms[sensorType]}

        </AddSensorContainer>

    );
};

export default AddSensorView