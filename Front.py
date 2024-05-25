from flask import Flask, render_template, request
from rdflib import Graph
from rdflib import Namespace
import numpy as np

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("web.html")
    elif request.method == "POST":
        substring = "rdflib.term.Literal"
        g = Graph()
        g.parse("data.ttl", format="ttl")
        qres = []
        base_iri = "http://www.semanticweb.org/ana/ontologies/2022/11/HarryPotterMovies#"

        if request.form["submit_button"] == "The House with the most females":
            query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                 SELECT ?House_With_Most_Females (COUNT(?gender) AS ?FemaleCount) WHERE
                  {
                        ?character rdf:type :Character;
                            :BelongsToHouse ?House_With_Most_Females.
                        ?character :hasGender ?gender.
                        FILTER (?gender= "Female")
                    } GROUP BY ?House_With_Most_Females
                    ORDER BY DESC(?FemaleCount)
                    LIMIT 1
            
            """
            qres = g.query(query)
            qres = [{"sub": row.House_With_Most_Females.replace(base_iri, " "), "ob": row.FemaleCount.replace(base_iri, ":")} for row in qres]
            return render_template("page1.html", queryRes=qres)

        elif request.form["submit_button"] == "Wizards who are male and pureblood":
            query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            select ?Wizards ?Gender ?Blood_Status  where{
                ?Wizards rdf:type :Character;
                        :hasGender ?Gender
                FILTER (?Gender = "Male")
                ?Wizards  :hasBloodStatus ?Blood_Status
                FILTER (?Blood_Status =:Pure_blood)
            }
            """
            qres = g.query(query)
            qres = [{"sub": row.Wizards.replace(base_iri, " "), "ob": row.Blood_Status.replace(base_iri, " ")} for row in qres]
            return render_template("page6.html", queryRes=qres)

        elif request.form["submit_button"] == "Which wizards have a Patronus":
            query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            select ?wizards ?patronus where{
                ?wizards :hasPatronus ?patronus
                FILTER (?patronus != :Unknown && ?patronus !=  :None)      
            }
            """
            qres = g.query(query)
            qres = [{"sub": row.wizards.replace(base_iri, " "), "ob": row.patronus.replace(base_iri, " ")} for row in qres]
            return render_template("page4.html", queryRes=qres)

        elif request.form["submit_button"] == "House that won most quidditch matches":
            query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            select ?VictoriousHouse (COUNT (?q1) AS ?WinnersCount) where 
            {
                ?participant rdf:type :Character ;
                            :BelongsToHouse ?VictoriousHouse.
                ?participant :quidditch_1996_1997 ?q1.                 
                filter (?q1 = "true"^^xsd:boolean)
            } 
            group by ?VictoriousHouse
            order by desc(?WinnersCount)
            LIMIT 1
            """
            qres = g.query(query)
            qres = [{"sub": row.VictoriousHouse.replace(base_iri, " "), "ob": row.WinnersCount} for row in qres]
            return render_template("page5.html", queryRes=qres)

        elif request.form["submit_button"] == "What are the effects of a certain spell":
            query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?Curses ?Effect
            where{
                ?Curses rdf:type :Spell.
                filter (REGEX(STR(?Curses), "Curse") )
                ?Curses :hasEffect ?Effect.           
            }
            """
            qres = g.query(query)
            qres = [{"sub": row.Curses.replace(base_iri, " "), "ob": row.Effect.replace(base_iri, " ")} for row in qres]
            return render_template("page2.html", queryRes=qres)

        elif request.form["submit_button"] == "Students whose wands were 10 inches long":
            query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            SELECT ?student ?wandLength WHERE {
                ?student :hasJob :Student. 
                ?student :hasWand ?wand .
                BIND (REGEX(STR(?wand), "10") AS ?wandLength)
                FILTER (?wandLength=true).
            }
            """
            qres = g.query(query)
            qres = [{"sub": row.student.replace(base_iri, " "), "ob": row.wandLength.replace(base_iri, " ")} for row in qres]
            return render_template("page3.html", queryRes=qres)

if __name__ == "__main__":
    app.run(debug=True, port=8000)

