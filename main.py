from typing import List

from fastapi import FastAPI, HTTPException, status, Depends

from fastapi.middleware.cors import CORSMiddleware

from schemas import BaseProduct, BaseUser, Order, OrderItem, Product, User, CreateUser, CreateOrder

from sqlalchemy.orm import Session

from database import engine, get_db

import datetime

import models

from dotenv import load_dotenv
load_dotenv()

models.Base.metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/users", response_model=List[User], status_code=200, tags=['User'])
def get_users(db: Session = Depends(get_db)):
    db_users = db.query(models.User).all()
    return [User(**user.__dict__) for user in db_users]


@app.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK, tags=['User'])
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Usuário não encontrado")
    return User(**db_user.__dict__)


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=['User'])
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")
    new_user = user.dict()
    db_new_user = models.User(**new_user)
    db.add(db_new_user)
    db.commit()
    db.refresh(db_new_user)
    return User(**db_new_user.__dict__)


@app.put("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK, tags=['User'])
def update_user(user: BaseUser, user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")
    db_update_user = db.query(models.User).filter(
        models.User.id == user_id).first()
    if db_update_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Usuário não encontrado")
    db_update_user.name = user.name
    db_update_user.email = user.email
    db_update_user.role = user.role
    db_update_user.active = user.active
    db.commit()
    db.refresh(db_update_user)
    return User(**db_update_user.__dict__)


@app.delete("/users/{user_id}", response_model=str, status_code=status.HTTP_200_OK, tags=['User'])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Usuário não encontrado")
    db.delete(db_user)
    db.commit()
    return "ok"


@app.get("/login", response_model=User, status_code=status.HTTP_200_OK, tags=['Login'])
def log_in(
    email_user: str,
    password: str,
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(
        models.User.email == email_user,
        models.User.password == password).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autorizado")
    return User(**db_user.__dict__)


@app.get("/products", response_model=List[Product], status_code=200, tags=['Product'])
def get_products(db: Session = Depends(get_db)):
    db_products = db.query(models.Product).all()
    return [Product(**product.__dict__) for product in db_products]


@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED, tags=['Product'])
def create_product(product: BaseProduct, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(
        models.Product.name == product.name).first()
    if db_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Produto já cadastrado")
    new_product = product.dict()
    db_new_product = models.Product(**new_product)
    db.add(db_new_product)
    db.commit()
    db.refresh(db_new_product)
    return Product(**db_new_product.__dict__)


@app.put("/products/{product_id}", response_model=Product, status_code=status.HTTP_200_OK, tags=['Product'])
def update_product(product: BaseProduct, product_id: int, db: Session = Depends(get_db)):
    db_update_product = db.query(models.Product).filter(
        models.Product.id == product_id).first()
    if db_update_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Produto não encontrado")
    db_update_product.name = product.name
    db_update_product.description = product.description
    db_update_product.price = product.price
    db_update_product.type = product.type
    db.commit()
    db.refresh(db_update_product)
    return Product(**db_update_product.__dict__)


@app.delete("/products/{product_id}", response_model=str, status_code=status.HTTP_200_OK, tags=['Product'])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(
        models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Produto não encontrado")
    db.delete(db_product)
    db.commit()
    return "ok"


@app.get("/orders", response_model=List[Order], status_code=200, tags=['Order'])
def get_orders(db: Session = Depends(get_db)):
    db_orders: List[models.Order] = db.query(models.Order).order_by(models.Order.order_number).all()
    return [Order(
        order_number=db_order.order_number,
        status=db_order.status,
        date=db_order.date,
        items=[OrderItem(name=db_order_item.product.name)
               for db_order_item in db_order.items]
    ) for db_order in db_orders]


@app.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED, tags=['Order'])
def create_order(order: CreateOrder, db: Session = Depends(get_db)):
    db_new_order = models.Order(
        status="pendente",
        date=datetime.datetime.now().date().strftime('%m/%d/%Y'),
        items=[models.OrderItem(product_id=order_item.product_id) for order_item in order.items]
    )
    db.add(db_new_order)
    db.commit()
    db.refresh(db_new_order)
    return Order(
        order_number=db_new_order.order_number,
        status=db_new_order.status,
        date=db_new_order.date,
        items=[OrderItem(name=db_order_item.product.name)
               for db_order_item in db_new_order.items]
    )

@app.put("/orders", response_model=Order, status_code=status.HTTP_201_CREATED, tags=['Order'])
def update_order(order_number: int, current_status: str, db: Session = Depends(get_db)):
    db_update_order = db.query(models.Order).filter(models.Order.order_number == order_number).first()
    if db_update_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Pedido não encontrado")
    db_update_order.date = datetime.datetime.now().date().strftime('%m/%d/%Y'),
    db_update_order.status = 'em andamento' if current_status == 'pendente' else 'concluido'
    db.commit()
    db.refresh(db_update_order)
    return Order(
        order_number=db_update_order.order_number,
        status=db_update_order.status,
        date=db_update_order.date,
        items=[OrderItem(name=db_order_item.product.name)
               for db_order_item in db_update_order.items]
    )
