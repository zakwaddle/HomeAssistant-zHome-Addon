import React, {useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import useApi from "./useApi";
import {globalStateActions} from "../store/globalStateSlice";


const useDevices = () => {
    const dispatch = useDispatch();
    const shouldUpdateDevices = useSelector(state => state['globalState']['shouldUpdateDevices'])
    const selectedDevice = useSelector(state => state['globalState']['selectedDevice'])
    const {fetchDevices} = useApi();
    useEffect(() => {

        if (shouldUpdateDevices){
            let selectedDeviceId
            if(selectedDevice){
                selectedDeviceId = selectedDevice.id
            }
            fetchDevices().then(data => {
                const newDevices = data.filter(device => device.display_name === null)
                // const devices = data.filter(device => device.display_name !== null)
                const devices = data
                if (selectedDeviceId){
                    const selected = data.filter(device => device.id === selectedDeviceId)
                    selected && dispatch(globalStateActions.updateSelectedDevice(selected[0]))
                }

                dispatch(globalStateActions.updateDevices(devices));
                dispatch(globalStateActions.updateNewDevices(newDevices));
                dispatch(globalStateActions.updateShouldUpdateDevices(false));
            });
        }
    }, [shouldUpdateDevices]);

}

export default useDevices;