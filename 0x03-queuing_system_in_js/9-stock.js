const express = require("express");
const { createClient } = require("redis");
const { promisify } = require("util");

const app = express();
const port = 1245;
const redisClient = createClient();

const asyncSet = promisify(redisClient.set).bind(redisClient);
const asyncGet = promisify(redisClient.get).bind(redisClient);

const listProducts = [
  { id: 1, name: "Suitcase 250", price: 50, stock: 4 },
  { id: 2, name: "Suitcase 450", price: 100, stock: 10 },
  { id: 3, name: "Suitcase 650", price: 350, stock: 2 },
  { id: 4, name: "Suitcase 1050", price: 550, stock: 5 },
];

const getItemById = (id) => {
  const product = listProducts.find((element) => element.id === Number(id));
  return product;
};

const reserveStockById = async (itemId, stock) => {
  try {
    await asyncSet(itemId, stock);
  } catch (err) {
    console.error(err);
  }
};

const getCurrentReservedStockById = async (itemId) => {
  const stock = await asyncGet(itemId);
  if (stock === null) {
    throw new Error("Not found");
  }
  return stock;
};

// Lists all products data
app.get("/list_products", (req, res) => {
  const productsData = [];
  listProducts.forEach((product) => {
    const productJson = {
      itemId: product.id,
      itemName: product.name,
      price: product.price,
      initialAvailableQuantity: product.stock,
    };
    productsData.push(productJson);
  });
  res.status(200).json(productsData);
});

// Lists products data based on the Id passed in the req args
app.get("/list_products/:itemId", async (req, res) => {
  const { itemId } = req.params;
  try {
    const stock = await getCurrentReservedStockById(itemId);
    const parseStock = JSON.parse(stock);
    const resJsonData = {
      itemId: parseStock.id,
      itemName: parseStock.name,
      price: parseStock.price,
      initialAvailableQuantity: parseStock.stock,
    };
    res.status(200).json(resJsonData);
  } catch (err) {
    res.status(404).json({ status: "Product not found" });
  }
});

// Reserves a product to a costumer if product exists and
// still available in the stock
app.get("/reserve_product/:itemId", async (req, res) => {
  const { itemId } = req.params;
  const product = getItemById(itemId);
  if (!product) {
    return res.status(404).json({ status: "Product not found" });
  }
  if (product.stock < 1) {
    return res
      .status(401)
      .json({ status: "Not enough stock available", itemId: itemId });
  }
  try {
    await reserveStockById(itemId, JSON.stringify(product));
    return res
      .status(200)
      .json({ status: "Reservation confirmed", itemId: itemId });
  } catch (err) {
    console.error(err);
  }
});

app.listen(port);
