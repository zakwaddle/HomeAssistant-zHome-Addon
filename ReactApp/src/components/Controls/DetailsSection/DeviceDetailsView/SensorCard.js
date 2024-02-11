import styled from "styled-components";
import {useDispatch} from "react-redux";
import {globalStateActions} from "../../../../store/globalStateSlice";
import React from "react";

const SensorContainer = styled.div`
  border: 1px solid grey;
  border-radius: 1em;
  padding: .5em;
  margin: .25em;
`

const SensorCard = ({sensorDetails}) => {
    const {name, sensor_type, sensor_config} = sensorDetails
    const title = {
        'motion': 'Motion Sensor',
        'led': 'LED Dimmer',
        'weather': 'Weather Sensor',
    }

    const dispatch = useDispatch()
    const setSensorView = () => dispatch(globalStateActions.updateDetailsSectionView('sensor'))
    const setSelectedSensor = () => dispatch(globalStateActions.updateSelectedSensor(sensorDetails))
    const handleClick = () => {
        setSelectedSensor()
        setSensorView()
    }
    return (
        <SensorContainer onClick={handleClick}>
            <h4>{title[sensor_type]}</h4>
            <p><b>{name}</b></p>
            <p>Pin: {sensor_config.pin}</p>
        </SensorContainer>
    )
}

export default SensorCard;