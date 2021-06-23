  
### Test Description 📜 :   /register [method = POST] 

- #### Positive Tests ✅ : 

    - **Screenshot/gif** 📸 :
    <br>

    ![post-register-positive](https://user-images.githubusercontent.com/56113566/120222706-01edad00-c25e-11eb-96b0-d0a6d62534e8.gif)

    - **Expected Result** 📝 : A new user should be created.

    <br> 

    - **Screenshot/gif** 📸 :

    <br> 

    ![register-positive-1](https://user-images.githubusercontent.com/56113566/120224846-d7055800-c261-11eb-8989-2d8da8de84c1.png)

    - **Expected Result** 📝 : A new user should be created.
    <br>

    ![register-positive-1-res](https://user-images.githubusercontent.com/56113566/120224850-d8cf1b80-c261-11eb-8801-59f7fa4a3fa5.png)
    
    <br> 

    - **Screenshot/gif** 📸 :
    <br> 

    ![register-positive-2](https://user-images.githubusercontent.com/56113566/120225485-f8b30f00-c262-11eb-85d6-4805e2620372.png)

    - **Expected Result** 📝 : A new user should be created.
    <br>

    ![register-positive-1-res](https://user-images.githubusercontent.com/56113566/120224850-d8cf1b80-c261-11eb-8801-59f7fa4a3fa5.png)

    <br>

- #### Negative Tests ❌ : 


    - **Screenshot/gif** 📸 :
        - If a username **already exists**.
    <br>

    ![register-negative-6](https://user-images.githubusercontent.com/56113566/120224858-dc62a280-c261-11eb-84dd-7d1014b43b7e.png)

    - **Expected Result** 📝 : A new user shouldn't be created.
    <br>

    ![register-negative-6-res](https://user-images.githubusercontent.com/56113566/120224864-de2c6600-c261-11eb-8e7b-391be3281f6d.png)

    <br>

    - **Screenshot/gif** 📸 :
        - If user email **already exists**.
    <br>

    ![register-negative-7](https://user-images.githubusercontent.com/56113566/120224867-df5d9300-c261-11eb-900c-b8ef91aa3ae4.png)

    - **Expected Result** 📝 : A new user shouldn't be created.
    
    <br>

    ![register-negative-7-res](https://user-images.githubusercontent.com/56113566/120224876-e4224700-c261-11eb-8c6c-792e1e51289f.png)



    - **Screenshot/gif** 📸 :
        - If name attribute is **invalid**.
    <br>
    
    ![post-register-negative-1](https://user-images.githubusercontent.com/56113566/120222960-6f014280-c25e-11eb-8aa8-691fec8c8e8b.png)

    - **Expected Result** 📝 : A new user shouldn't be created.
    
    <br>

    ![post-register-negative-1-res](https://user-images.githubusercontent.com/56113566/120222966-745e8d00-c25e-11eb-99ec-5054111a0957.png)

    <br>

    - **Screenshot/gif** 📸 :
        - If user email is **invalid**.
    <br>
    
    ![post-register-negative-2](https://user-images.githubusercontent.com/56113566/120222980-79bbd780-c25e-11eb-9345-6e588e518cdf.png)
  
    - **Expected Result** 📝 : A new user shouldn't be created.
    <br>
    
    ![post-register-negative-2-res](https://user-images.githubusercontent.com/56113566/120222985-7aed0480-c25e-11eb-8156-e71a64c1ed92.png)

    <br>

    - **Screenshot/gif** 📸 :
        - Password field has to be at **least 8 characters**. 
    <br>

    ![post-register-negative-3](https://user-images.githubusercontent.com/56113566/120222996-804a4f00-c25e-11eb-910e-b93e97b44b45.png)

    - **Expected Result** 📝 : A new user shouldn't be created.
    <br>

    ![post-register-negative-3-res](https://user-images.githubusercontent.com/56113566/120222998-817b7c00-c25e-11eb-9d50-daded22e17ba.png)

    <br>

    - **Screenshot/gif** 📸 :
        - Username field has to be **atleast 5-25 characters**.
    <br>

    ![post-register-negative-4](https://user-images.githubusercontent.com/56113566/120223004-84766c80-c25e-11eb-8b3d-478c32473f1b.png)

    - **Expected Result** 📝 : A new user shouldn't be created.
    <br>

    ![post-register-negative-4-res](https://user-images.githubusercontent.com/56113566/120223012-86d8c680-c25e-11eb-9e11-381ca4d3b4f0.png)

    <br>

    - **Screenshot/gif** 📸 :
        - Terms and condition are **not checked**.
    <br>

    ![post-register-negative-5](https://user-images.githubusercontent.com/56113566/120223026-8b9d7a80-c25e-11eb-87b3-cf8b85ee742e.png)

    - **Expected Result** 📝 : A new user shouldn't be created.

    <br>

    ![post-register-negative-5-res](https://user-images.githubusercontent.com/56113566/120223043-91935b80-c25e-11eb-97be-fab631b367b7.png)
