import React from "react";
import styled from "styled-components";
import UpdateHostForm from "./UpdateHostForm";
import useApi from "../../../../hooks/useApi";
import {useDispatch, useSelector} from "react-redux";
import {globalStateActions} from "../../../../store/globalStateSlice";
// import {Button} from "../../../../styles/SectionStyles";

const Box = styled.div`
`

export default function UpdateHostView (){
    const {sendMessage} = useApi()
    const dispatch = useDispatch()
    const selectedDevice = useSelector(state => state['globalState']['selectedDevice'])
    const deviceDetailsView = () => dispatch(globalStateActions.updateDetailsSectionView('main'))

    const handleSubmit = (host) => {
        sendMessage(selectedDevice.id, {
            command: "update_host",
            host: host}).then(data => {
            console.log(data)
            deviceDetailsView()
        })
    }

    return (

            <UpdateHostForm submitHandler={handleSubmit} cancelHandler={deviceDetailsView}/>
    )
}