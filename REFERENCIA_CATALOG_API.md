# Referência - Facebook Catalog API

Este documento armazena as informações, tokens e exemplos de uso da Catalog API fornecidos.

## Tokens de Acesso
- `process.env.META_PAGE_ACCESS_TOKEN_DL`
- `process.env.META_PAGE_ACCESS_TOKEN_DL`

## IDs e Endpoints Básicos
- **Catalog ID:** `1783259002838364`
- **Consulta de Dados do Catálogo:** `1783259002838364?fields=id,name,product_count`

## Exemplos de cURL

### 1. Obter Informações do Catálogo
```bash
curl -i -G \
  'https://graph.facebook.com/v25.0/1783259002838364?fields=id,name,product_count' \
  -d 'access_token=process.env.META_PAGE_ACCESS_TOKEN_DL'
```

**Resposta Esperada:**
```json
{
  "name": "Product Catalog Name",
  "product_count": "<product_count>",
  "id": "<catalog_id>"
}
```

### 2. Criar Múltiplos Produtos em Lote (items_batch)
```bash
curl -i -X POST \
  'https://graph.facebook.com/v25.0/1783259002838364/items_batch' \
  -d 'item_type=PRODUCT_ITEM' \
  -d 'requests=[
  {
    "method": "CREATE",
    "data": {
      "id": "test_product_retailer_id_1",
      "title": "Product 1 Title",
      "description": "HTML <b>Description</b> of the Product 1",
      "price": "100.4 USD",
      "image_link": "image_url_for_product_1",
      "link": "website_url_for_product_1",
      "availability": "in stock",
      "condition": "new",
      "brand": "brand_name"
    }
  },
  {
    "method": "CREATE",
    "data": {
      "id": "test_product_retailer_id_2",
      "title": "Product 2 Title",
      "description": "HTML <b>Description</b> of the Product 2",
      "price": "120.4 USD",
      "image_link": "image_url_for_product_2",
      "link": "website_url_for_product_2",
      "availability": "in stock",
      "condition": "new",
      "brand": "brand_name_for_product_2"
    }
  }
]' \
  -d 'access_token=process.env.META_PAGE_ACCESS_TOKEN_DL'
```

**Resposta Esperada:**
```json
{
  "handles": [
    "{HANDLE_ID}"
  ]
}
```

### 3. Listar e Filtrar Produtos
```bash
curl -i -G \
 'https://graph.facebook.com/v25.0/1783259002838364/products' \
 -d 'filter={"name":{"i_contains":"title"}}' \
 -d 'fields=retailer_id,id,name,category,errors' \
 -d 'access_token=process.env.META_PAGE_ACCESS_TOKEN_DL'
```

**Resposta Esperada:**
```json
{
  "data": [
    {
      "retailer_id": "test_product_retailer_id_2",
      "id": "<PRODUCT_ID>",
      "name": "Product 2 Title"
    },
    {
      "retailer_id": "test_product_retailer_id_1",
      "id": "<PRODUCT_ID>",
      "name": "Product 1 Title"
    }
  ],
  "paging": {
    "cursors": {
      "before": "<prev_page_cursor>",
      "after": "<next_page_cursor>"
    },
    "next": "https://graph.intern.facebook.com/v22.0/{CATALOG_ID}/products?access_token={ACCESS_TOKEN}&fields=retailer_id,id,name,category,errors&filter={\"name\":{\"i_contains\":\"title\"}}&after={next_page_cursor}",
    "previous": "https://graph.intern.facebook.com/v22.0/{CATALOG_ID}/products?access_token={ACCESS_TOKEN}&fields=retailer_id,id,name,category,errors&filter={\"name\":{\"i_contains\":\"title\"}}&after={prev_page_cursor}"
  }
}
```

## Próximos Passos (Conforme Recomendação Meta)
- Consultar a [Developer Docs for Catalog API](https://developers.facebook.com/docs/commerce-platform/catalog)
- Utilizar SDKs para Python, Java, NodeJS ou PHP.
