const swaggerJsdoc = require("swagger-jsdoc");

const options = {
  definition: {
    openapi: "3.0.0",
    info: {
      title: "MS Juegos API",
      version: "1.0.0",
      description: "Documentación Swagger del microservicio de juegos",
    },
    servers: [
      {
        url: "http://localhost:8002",
        description: "Servidor local del microservicio juegos",
      },
    ],
    tags: [
      {
        name: "Juegos",
        description: "Operaciones relacionadas con juegos",
      },
    ],
  },
  apis: ["./src/routes/*.js"],
};

const swaggerSpec = swaggerJsdoc(options);

module.exports = swaggerSpec;
