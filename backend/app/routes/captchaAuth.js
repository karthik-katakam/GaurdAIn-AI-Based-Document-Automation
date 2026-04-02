require('dotenv').config();
const express = require('express')
const cors = require('cors')
const axios = require('axios')
const app = express()
const port = 8000

const SITE_SECRET = process.env.REACT_APP_SECRET_KEY

app.use(cors())
app.use(express.json())


app.post('/verify-captcha', async(request, response) =>
{
    const {captchaValue} = request.body;

    if(!captchaValue)
    {
        return response.status(400).json({success: false, message: 'Error: Captcha token not received'})
    }
    else
    {

    
    const {data} = await axios.post(`https://www.google.com/recaptcha/api/siteverify?secret=${SITE_SECRET}&response=${captchaValue}`,
    
    )
    console.log("Result:", data)
    console.log("SECRET: " + SITE_SECRET)

    response.send(data)
}})

app.listen(port, () => {
    console.log(`Server listening at ${port}`)
    if(SITE_SECRET)
    {
        console.log("SITE SECRET IS VALID")
    }

})