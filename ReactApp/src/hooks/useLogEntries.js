import React, {useEffect} from "react";
import {useDispatch} from "react-redux";
import {globalStateActions} from "../store/globalStateSlice";
import useApi from "./useApi";

export default function useLogEntries(){

    const dispatch = useDispatch();
    const {fetchLogs} = useApi();

    useEffect(() => {
        fetchLogs().then(data => {
            dispatch(globalStateActions.updateDeviceLogs(data))
        })
    }, []);
};