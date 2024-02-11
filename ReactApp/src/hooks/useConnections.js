import React, {useEffect} from "react";
import {useDispatch} from "react-redux";
import useApi from "./useApi";
import {globalStateActions} from "../store/globalStateSlice";


const useConnections = () => {
    const dispatch = useDispatch()

    const {
        fetchWifiNetworks,
        fetchFtpServers,
        fetchMqttBrokers,
    } = useApi()

    useEffect(() => {
        fetchWifiNetworks().then(data => {
            dispatch(globalStateActions.updateWifiNetwork(data[0]))
        })
        fetchFtpServers().then(data => {
            dispatch(globalStateActions.updateFtpServer(data[0]))
        })
        fetchMqttBrokers().then(data => {
            dispatch(globalStateActions.updateMqttBroker(data[0]))
        })
    }, [])
}

export default useConnections;