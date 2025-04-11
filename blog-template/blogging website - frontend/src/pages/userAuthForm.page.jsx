import InputBox from "../components/input.component";
import googleIcon from "../imgs/google.png";
const UserAuthForm = ({ type }) => {
    return (
        <section className="h-cover flex items-center justify-center">
            <form className="w-[80%] max-w-[400px]">
                <h1 className="text-4xl font-roboto capitalize
                text-center mb-24">
                    {type == "sign-in" ? "Welcome back" : "Join us today"}
                </h1>
                
                { 
                    type != "sign-in" ?
                    <InputBox
                        name="fullname"
                        type="text"
                        placeholder="Full Name"
                        icon="fi-rr-user"
                     />
                    : ""
                }

                <InputBox
                        name="email"
                        type="email"
                        placeholder="Email"
                        icon="fi-rr-envelope"
                     />
                <InputBox
                        name="password"
                        type="password"
                        placeholder="Password"
                        icon="fi-rr-key"
                />

                {/* Sign Up Button */}
                <button className="btn-dark py-2 w-full gap-4 mt-10 mb-4">
                    {type.replace("-", " ")}
                </button>

                {/* OR Divider */}
                <div className="flex items-center justify-center my-10 w-full gap-4">
                    <div className="h-px bg-black flex-1" />
                    <p className="text-black font-bold uppercase">or</p>
                    <div className="h-px bg-black flex-1" />
                </div>

                {/* Google Auth Button */}
                <button className="border-2 border-black text-black hover:bg-black hover:text-white font-semibold flex items-center justify-center gap-4 w-[90%] mx-auto py-2 rounded-full transition-colors">
                    <img src={googleIcon} className="w-5" alt="Google Icon" />
                    Continue with Google
                </button>

            </form>
        </section>
    );
}

export default UserAuthForm;