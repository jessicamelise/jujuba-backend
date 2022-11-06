```mermaid
erDiagram
    PRODUCT {
        number id
        string name
        string description
        string price
        string type
    }
    ORDER {
        number order_number
        string status
    }
    ORDER_ITEM {
        number order_number
        number product_id
        number id
    }
    ORDER ||--|{ ORDER_ITEM : contem
    ORDER_ITEM ||--|| PRODUCT : tem
```