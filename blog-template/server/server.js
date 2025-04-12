import express from 'express';
import mongoose from 'mongoose';
import 'dotenv/config';
import bcrypt from 'bcrypt';
import User from './Schema/User.js';
import { nanoid } from 'nanoid';

const server = express();
let PORT = 3000;

let emailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/; // regex for email
let passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/; // regex for password
let nameRegex = /^[a-zA-Z\s]+$/; // regex for full name (only letters and spaces)

server.use(express.json());

// Connect to MongoDB
mongoose.connect(process.env.DB_LOCATION, {
    autoIndex: true
});

const formatDatatoSend = (user) => {
    return {
        profile_img: user.personal_info.profile_img,
        fullname: user.personal_info.username,
        fullname: user.personal_info.fullname
    };
}

const generateUsername = async (email) => {
    let username = email.split("@")[0];

    let isUsernameNotUnique = await User.exists({ "personal_info.username": username }).then((result) => result)

    isUsernameNotUnique ? username += nanoid().substring(0, 5) : "";

    return username
    
}

server.post("/signup", (req, res) => {

    let { fullname, email, password } = req.body;

    if(fullname.length < 3){
        return res.status(403).json({ error: "Enter your full name" });
    }
    if(!email.length) {
        return res.status(403).json({ error: "Enter email" });
    }
    if(!emailRegex.test(email)) {
        return res.status(403).json({ error: "Enter valid email" });
    }
    if(!passwordRegex.test(password)) {
        return res.status(403).json({ error: "Password must contain at least one number, one uppercase and lowercase letter, and at least 6-20 characters" });
    }

    bcrypt.hash(password, 10, async (err, hashed_password) => {

        let username = await generateUsername(email); // get username from email
        
        let user = new User({
            personal_info: { fullname, email, password: hashed_password, username },    
        });

        try {
            user.save().then((u) => {
                return res.status(200).json({ user: u });
            }).catch(err => {
                console.log(err);
                return res.status(500).json({ error: "Internal server error" });
            });
        } catch (err) {

            if(err.code == 11000) {
                return res.status(500).json({ error: "Email already exists" });
            }
            console.log(err);
            return res.status(500).json({ error: "Internal server error" });
        }


        console.log(hashed_password);    
        });
    });

server.listen(PORT, () => {
    console.log(`Listening on port -> ${PORT}`);
})
