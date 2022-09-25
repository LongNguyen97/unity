# Installation
1. Clone the repository
   
2. At the folder, build the project using docker-compose:
   
    `docker-compose build; docker-compose up -d;`
   
    Now, the project is running successfully on http://localhost:8000.
    - To add new email using widget: open file `store.html` and fill email go register.
    - To check access list emails, go to: http://localhost:8000/stats/
    - To check the celery task runs at `08:00 AM` every `Monday` and `Wednesday`, execute the bellow command:
    
        `docker-compose logs -f celery`
     

 That's all for the project, thanks.