import React, {useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {globalStateActions} from "../store/globalStateSlice";
import useApi from "./useApi";

export default function useLogEntries(pollingSeconds=null){

    const dispatch = useDispatch();
    const {fetchLogs} = useApi();
    const shouldUpdateLogs = useSelector(state => state['globalState']['shouldUpdateLogs'])


    useEffect(() => {
        let timeout;
        if (shouldUpdateLogs) {
            fetchLogs().then(data => {
                dispatch(globalStateActions.updateDeviceLogs(data));
                dispatch(globalStateActions.updateShouldUpdateLogs(false));
                // console.log("checked for logs");
            });
        } else if (pollingSeconds) {
            timeout = setTimeout(
                () => dispatch(globalStateActions.updateShouldUpdateLogs(true)),
                pollingSeconds * 1000);
        }

        // Cleanup function to clear the timeout
        return () => clearTimeout(timeout);
    }, [shouldUpdateLogs]);

};