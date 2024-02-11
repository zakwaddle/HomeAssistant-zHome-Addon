import React from "react";
// import styled from 'styled-components';
import {useSelector} from "react-redux";
import DeviceDetailsView from "./DeviceDetailsView";
import SensorDetails from "./SensorDetailsView/SensorDetails";
import AddSensorView from "./AddSensorView";
import UpdateHostView from "./UpdateHostView";


const Wrapper = ({children}) => {
    return ({...children})
}

export default function DetailSection (){
    const selectedDevice = useSelector(state => state['globalState']['selectedDevice'])
    const menuSelection = useSelector(state => state['globalState']['menuSelection'])
    const sectionView = useSelector(state => state['globalState']['detailsSectionView'])

    const isVisible = menuSelection === 'Devices'
    if (!selectedDevice || !isVisible) {
        return null
    }
    const detailsViews = {
        'main': <DeviceDetailsView/>,
        'sensor': <SensorDetails/>,
        'addSensor': <AddSensorView/>,
        'updateHost': <UpdateHostView/>
    }
    return (
        <Wrapper>
            {detailsViews[sectionView]}
        </Wrapper>
    )
}