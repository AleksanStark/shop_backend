from litestar import Litestar, post, MediaType
from litestar.config.cors import CORSConfig
from pydantic import BaseModel
import stripe
import uvicorn



# Stripe API Key
stripe.api_key = "sk_test_51QH1RuAGiLDyLsr1ht1TxBc3rUb483621kVYgKO2he4C75W6jZdFrr2DwjRFoGdN85fhboRyX636gHHPiNbr14yf001GoOfBqp"

# CORS Configuration
cors_config = CORSConfig(
    allow_origins=["http://localhost:3000", "https://shop-os1pyynkd-alex240941123gmailcoms-projects.vercel.app"],  # Replace with actual frontend origin
    allow_methods=["POST"],  # Restrict methods if needed
    allow_credentials=True,
    allow_headers=["*"],
)

# Define the input schema using Pydantic
class Items(BaseModel):
    line_items: list[dict]

# Route handler for Stripe checkout session
@post("/checkout", media_type=MediaType.JSON)
async def create_checkout_session(data: Items) -> dict:
    try:
        # Log incoming data for debugging
        print(data)

        # Create a checkout session with Stripe
        session = stripe.checkout.Session.create(
            line_items=data.line_items,
            mode="payment",
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",
        )

        # Return the session URL
        return {"sessionId": session.id}
    except Exception as e:
        # Log and return an error response
        print(data)
        print(f"Error creating checkout session: {e}")
        return {"error": str(e)}, 500

# Initialize Litestar application
app = Litestar(route_handlers=[create_checkout_session], cors_config=cors_config)
uvicorn.run(app, host="0.0.0.0", port=8000)


  