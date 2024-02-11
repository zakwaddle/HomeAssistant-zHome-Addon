import React from "react";
// import styled from 'styled-components';
import {DeviceList} from "./DevicesInfoView/DeviceList";
import ConnectionSection from "./ConnectionsInfoView";
import {useSelector} from "react-redux";

const Wrapper = ({children}) => {
    return ({...children})
}
export default function InfoWindow (){
    const menuSelection = useSelector(state => state['globalState']['menuSelection'])

    const infoSection = {
        "Devices": <DeviceList/>,
        "Connections": <ConnectionSection/>
    }

    return (
        <Wrapper>
            {infoSection[menuSelection]}
        </Wrapper>
    )
}