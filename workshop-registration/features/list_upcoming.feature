Feature: List all upcoming workshops

    @skip
    Scenario: Do not list past workshops

    Scenario: Provide the right registration summary (registration link, number of approved and waiting registrants, number of free spots) of workshops
        Given the following people registered for workshop at link "www.ibots.de" with a capacity of 5 participants:
            | name  | status     | link          |
            | alice | approved   | www.ibots.de  |
            | betty | waitlisted | www.ibots.de  |
            | cathy | approved   | www.ibots.de  |
            | denis | rejected   | www.ibots.de  |
            | eve   | waitlisted | www.ibots.de  |
            | ford  | approved   | www.ibots.de  |
            | gemma | rejected   | www.ibots.de  |
            | henry | approved   | www.ibots.de  |
        When the user checks upcoming workshops
        Then they see the following worshops registration summary:
            | link          | num_approved | num_waitlisted | num_rejected | num_free_spots |
            | www.ibots.de  | 4            | 2              | 2            | 1              |
            
        
    
    Scenario Outline: List workshops created by any member in the team
        Given Mohammad has workshops <Mohammad> 
        And Sangeetha has workshops <Sangeetha>
        And Nick has workshops <Nick>
        When the user checks upcoming workshops
        Then they see a list containing workshops <Mohammad>
        And they see a list containing workshops <Sangeetha>
        And they see a list containing workshops <Nick>

        Examples:
            | Mohammad | Sangeetha | Nick |
            | A        | B         |  -   |
            | C        | D         |  G   |
            | A,B      | D         |  H   |
            | -        | D         |  H   |

    Scenario Outline: List single workshop main details (registration link, title, date)
        Given one workshop with registration link "<link>", title "<title>", and date "<date>"
        When the user checks upcoming workshops
        Then they see workshops' details ("<link>", "<title>", "<date>")

        Examples:
            | link | title | date |
            | https://workshop-register.com/upcoming1 | Introduction to Python | 2023-09-15 |
            | https://workshop-register.com/upcoming2 | Intro to Rust | 2025-10-01 |


    Scenario: List multiple workshops' main details (registration link, title, date)
        Given the following workshops exist:
            | link                                   | title              | date       |
            | https://workshop-register.com/upcoming1 | Introduction to Python | 2023-09-15 |
            | https://workshop-register.com/upcoming2 | Intro to Rust       | 2025-10-01 |
        When the user checks upcoming workshops
        Then they see the following workshops' details:
            | link                                   | title              | date       |
            | https://workshop-register.com/upcoming1 | Introduction to Python | 2023-09-15 |
            | https://workshop-register.com/upcoming2 | Intro to Rust       | 2025-10-01 |




    @skip
    Scenario: Do not list non-workshop meetings

    @skip
    Scenario: Do not list non-host meetings