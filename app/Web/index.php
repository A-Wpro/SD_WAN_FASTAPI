<!DOCTYPE html>
<html>
    <head>
    <style>
        #TITLE {
            text-align: center;
             color:blue;
        }
        #ONOS {
            color:blue;
        }

        #section-1 {background-color: bisque;}
        nav {float: left; border:30px;}

        .flex-container {
            display: flex;
            flex-direction: row;
            font-size: 10px;
            text-align: center;
            }
        .flex-item-left{
            background-color: #f1f1f1;
            padding: 10px;
            flex: 50%;
        }
        .flex-item-center{
            background-color: #f1f1f1;
            padding: 10px;
            flex: 50%;
        }
        .flex-item-right{
            background-color: #f1f1f1;
            padding: 10px;
            flex: 50%;

        }



        .RESULTS {
            display: flex;
            flex-direction: row;
            font-size: 10px;
            text-align: center;
            background-color: white;
            }
    </style>

        <title>PROJET_SD_WAN</title>
    </head>


    <body>
        <h1 id="TITLE">
            PROJET_SD_WAN
        </h1>

        <div class="flex-container">

            <div class="flex-item-left">
                <button onclick="window.location.href='/'">
                    <h1>
                        Deploy Onos
                    </h1>

                </button>
            </div>

            <div class="flex-item-center">
                <button onclick="window.location.href='/GenerateOnosStruc'">
                <h1 class="ONOS">
                    Deploy RL
                </h1>
                </button>
            </div>

            <div class="flex-item-right">
            <button>
                <h1 class="ONOS">
                    Summary
                    <?php echo "test pho"

                    ?>
                </h1>
            </button>
            </div>

        </div>
        <div class="RESULTS">
            <div class="flex-item-center">

                <!-- essayer d inserer la commande mysql ici -->
                <h1 id="GET_GR_ID">

                <?php
                    echo "Jello";
                ?>
                

                </h1>
                
                
            </div>

        </div>

<!-- TODO : create script that changed the value of h1 to a sentence with id of graph -->
        <script>
            
            document.getElementById("GET_GR_ID").innerHTML = "Hello JavaScript!";
        </script>


    </body>

</html>