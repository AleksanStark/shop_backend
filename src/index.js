const express = require("express");
const cors = require("cors");
const pino = require("pino-http");
const stripe = require("stripe")(
  "sk_test_51QH1RuAGiLDyLsr1ht1TxBc3rUb483621kVYgKO2he4C75W6jZdFrr2DwjRFoGdN85fhboRyX636gHHPiNbr14yf001GoOfBqp"
);
const app = express();

app.use(express.json());
app.use(cors());
app.use(pino());

app.post("/checkout", async (req, res) => {
  console.log(req.body);
  try {
    const session = await stripe.checkout.sessions.create({
      line_items: req.body,
      mode: "payment",
      success_url: "http://localhost:3000/success",
      cancel_url: "http://localhost:3000/cancel",
    });
    res.json({ checkoutUrl: session.url, sessionId: session.id });
  } catch (err) {
    console.log(err);
  }
});

app.listen(8000, () => console.log("server runnig on 8000 port"));
