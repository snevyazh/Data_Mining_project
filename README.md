

# Finance.yahoo.com webscrapper

This is a code to scrap the news from finance.yahoo.com

1) it first opens the page and scraps all the news articles

2) the finance.yahoo.com has no paginator, but loads new content once the 
user is reaching the edge. So, the scrapper emulates this behaviour with
Selenium package

3) the news are filtered by &&&&&

4) for every news article we gets author, date and news text

## Authors

- [@kuzmatsukanov] (https://github.com/kuzmatsukanov)
- [@snevyazh] (https://github.com/snevyazh/)


## API Reference for future use in the project

#### Get all items

```http
  GET /api/items
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Get item

```http
  GET /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### add(num1, num2)

Takes two numbers and returns the sum.


## Appendix

Any additional information goes here

=======
# Data_Mining_project
the is for Data Mining Project 

