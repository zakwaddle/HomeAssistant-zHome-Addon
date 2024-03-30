import React, {useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import useApi from "./useApi";
import {globalStateActions} from "../store/globalStateSlice";


const useDevices = (pollingSeconds) => {
    const dispatch = useDispatch();
    const shouldUpdateDevices = useSelector(state => state['globalState']['shouldUpdateDevices'])
    const selectedDevice = useSelector(state => state['globalState']['selectedDevice'])
    const {fetchDevices} = useApi();

    useEffect(() => {
        let timeout;
        if (shouldUpdateDevices) {
            let selectedDeviceId = selectedDevice ? selectedDevice.id : null;
            fetchDevices().then(data => {
                const devices = data;
                if (selectedDeviceId) {
                    const selected = devices.find(device => device.id === selectedDeviceId);
                    if (selected) dispatch(globalStateActions.updateSelectedDevice(selected));
                }
                dispatch(globalStateActions.updateDevices(devices));
                dispatch(globalStateActions.updateShouldUpdateDevices(false));
                // console.log("updated devices")
            });
        } else if (pollingSeconds){
            timeout = setTimeout(
                () => dispatch(globalStateActions.updateShouldUpdateDevices(true)),
                pollingSeconds * 1000);
        }

        return () => clearTimeout(timeout);
    }, [shouldUpdateDevices]);


}

export default useDevices;