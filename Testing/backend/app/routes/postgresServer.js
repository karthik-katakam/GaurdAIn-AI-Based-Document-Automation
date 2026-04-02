const express = require('express')
const cors = require('cors')
const postgresPool = require('pg').Pool
const app = express()
const bodyParser = require("body-parser")
const port = 5000

app.use(cors())
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({extended:true}))

app.listen(port, (err)=>{
    if(err){
        console.log(err);
    }
    else{
    console.log(`Server is running on port ${port}`)
    }
})

const pool = new postgresPool({
        user: "njcourtsuser",
        password: "guardAInw@tch!",
        database: "guardAInWatchdb",
        host: "postgres",
        port: 5432
})

pool.connect((err, connection)=>{
   if(err)
    {
        console.log(err)
    } 

    else{
        console.log("Successfully connected to Database!")
    }
})


app.get("/case-detail", (req, res)=>{
    const sql = "SELECT * FROM case_detail ";
    pool.query(sql, (err, result)=>{
        if(err) {
            return res.json(err);
        }

        else{
            return res.status(200).json(result.rows)
        }
     })
    })

app.get("/case-detail/:id", (req, res)=>{
    const caseDetailID=Number(req.params.id)
    const sql = "SELECT * FROM case_detail WHERE id=$1";
    pool.query(sql,[caseDetailID], (err, result)=>{
        if(err) {
            return res.json(err);
        }

        else{
            return res.status(200).json(result.rows[0])
        }
        })
    })

app.get("/cases/", (req, res)=>{
    const sql = "SELECT * FROM cases ";
    pool.query(sql, (err, result)=>{
        if(err) {
            return res.json(err);
        }

        else{
            return res.status(200).json(result.rows)
        }
        })
    })


    app.get("/case-count", (req, res)=>{
        const sql = "SELECT * FROM case_count ";
        pool.query(sql, (err, result)=>{
            if(err) {
                return res.json(err);
            }
    
            else{
                return res.status(200).json(result.rows)
            }
         })
        })


        // app.post("/case-detail", (req, res)=>{
        //     const sql = "INSERT INTO case_detail(docketNum, caseName, date, description, caseType, status, parties, AIP, isProposedGuardian, otherGuardians, allGuardians, interpreterNeeded, interpreterPersonLanguage, disabilityAccommodation, accommodationParty, signature) ";
        //     pool.query(sql, (err, result)=>{
        //         if(err) {
        //             return res.json(err);
        //         }
        
        //         else{
        //             return res.status(200).json(result.rows)
        //         }
        //      })
        //     })

        



/*
CREATE TABLE case_detail (
    docketNum int,
    caseName varchar(255),
    date DATE,
    description varchar(255),
    caseType varchar(255),
	status varchar(255),
	parties varchar(255),
	AIP varchar(255),
	isProposedGuardian varchar(255),
	otherGuardians varchar(255),
	allGuardians varchar(255),
	interpreterNeeded varchar(255),
	interpreterPersonLanguage varchar(255),
	disabilityAccommodation varchar(255),
	accommodationParty varchar(255),
	signature varchar(255)
	
);*/