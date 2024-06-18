# [SkinMatch - C241-PS246] ML Model API
The ML model API provides product recommendation system, product list based on skin type, and compatible prediction.

# Deploy Link
Database (Auth API): https://auth-api-dczyyawmja-et.a.run.app

ML API: https://ml-api-dczyyawmja-et.a.run.app

## List of Available Endpoint
    1. /check_compatibility
    2. /product-rec-list
    3. /product-rec-byname
    4. /upload

## Endpoint List
### Compatibility

* Endpoint:
    * `POST /check_compatibility`

* Params: 
  * ingredient_to_check : ingredient results from images ocr
  
* Request Header
    * Content-Type : application/json
    * Authorization : Bearer <token>

* Response:
```json
{
    "result":"Not compatible because {ingredient} is an avoided ingredient."
}
```
* Other response:
```json
{
    "result":"Compatible!"
}
```
```json
{
    "result":"Not compatible because {ingredient} is not recommended for {skin_type} skin type."
}
```

### Product list based on skin type

* Endpoint:
    * `GET /product-rec-list`


* Params: 
  * skin-type : dry or from user profile

* Request Header
    * Content-Type : application/json
    * Authorization : Bearer <token>

* Response:
```json
[
    {
        "Brand": "LA MER",
        "Combination": 1,
        "Dry": 1,
        "Ingredients": "Algae (Seaweed) Extract, Mineral Oil, Petrolatum, Glycerin, Isohexadecane, Microcrystalline Wax, Lanolin Alcohol, Citrus Aurantifolia (Lime) Extract, Sesamum Indicum (Sesame) Seed Oil, Eucalyptus Globulus (Eucalyptus) Leaf Oil, Sesamum Indicum (Sesame) Seed Powder, Medicago Sativa (Alfalfa) Seed Powder, Helianthus Annuus (Sunflower) Seedcake, Prunus Amygdalus Dulcis (Sweet Almond) Seed Meal, Sodium Gluconate, Copper Gluconate, Calcium Gluconate, Magnesium Gluconate, Zinc Gluconate, Magnesium Sulfate, Paraffin, Tocopheryl Succinate, Niacin, Water, Beta-Carotene, Decyl Oleate, Aluminum Distearate, Octyldodecanol, Citric Acid, Cyanocobalamin, Magnesium Stearate, Panthenol, Limonene, Geraniol, Linalool, Hydroxycitronellal, Citronellol, Benzyl Salicylate, Citral, Sodium Benzoate, Alcohol Denat., Fragrance.",
        "Label": "Moisturizer",
        "Name": "Crème de la Mer",
        "Normal": 1,
        "Oily": 1,
        "Price": 175,
        "Rank": 4.1,
        "Sensitive": 1
    },
    {
        "Brand": "SK-II",
        "Combination": 1,
        "Dry": 1,
        "Ingredients": "Galactomyces Ferment Filtrate (Pitera), Butylene Glycol, Pentylene Glycol, Water, Sodium Benzoate, Methylparaben, Sorbic Acid.",
        "Label": "Moisturizer",
        "Name": "Facial Treatment Essence",
        "Normal": 1,
        "Oily": 1,
        "Price": 179,
        "Rank": 4.1,
        "Sensitive": 1
    }
]
```

### Recommendation System

* Endpoint:
    * `POST /product-rec-byname`

* Request Body: 
```json
{
    "product_name": "Moisture Surge 72-Hour"
}
```
* Response:
```json
{
    "Moisture Surge Intense Skin Fortifying Hydrator",
    "Moisture Surge Overnight Mask",
    "Moisture Surge Hydrating Supercharged Concentrate",
    "Moisture Mask",
    "Moisture Surge CC Cream Hydrating Colour Corrector Broad Spectrum SPF 30",
    "Total Replenishing Eye Cream",
    "Auto Correct Brightening and Depuffing Eye Contour Cream",
    "White Lucent Luminizing Surge",
    "Counter Balance™ Oil Control Hydrator",
    "Cucumber Gel Mask Extreme Detoxifying Hydrator"
}
```

### Image Save

* Endpoint:
    * `POST /upload`

* Request Body: 
    * form-data
        * key : file - File
        * Value : <image>
* Response:
```json
{
    "message": "File successfully uploaded",
    "url": "https://storage.googleapis.com/..."
}
```

