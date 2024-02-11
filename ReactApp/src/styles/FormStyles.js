import styled from "styled-components";

const FormLabel = styled.label`
  display: flex;
  justify-content: space-between;
  align-items: center;
  
`
const FormInput = styled.input`
  font-size: inherit;
  font-family: inherit;
`
const FormContainer = styled.form`
  display: flex;
  flex-direction: column;
  flex: 1 0;
`

export {FormInput, FormLabel, FormContainer};