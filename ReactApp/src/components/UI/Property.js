import styled from "styled-components";
import React from "react";

const PropertyRow = styled.div`
  width: 95%;
  display: flex;
  justify-content: space-between;
  padding-left: 1em;
  padding-right: 1em;
  //user-select: none;
`
const PropertyName = styled.div`

`
const PropertyValue = styled.div`

`
export const Property = ({name, value}) => {
    return (
        <PropertyRow>
            <PropertyName><b>{name}</b></PropertyName>
            <PropertyValue>{value}</PropertyValue>
        </PropertyRow>
    )
}

const PropStackContainer = styled.div`
  display: flex;
  flex-direction: column;
  //user-select: none;
`
export const PropStack = ({label, children}) => {
    return (
        <PropStackContainer>
            <p><b>{label}</b></p>
            <p>{children}</p>
        </PropStackContainer>
    )
}