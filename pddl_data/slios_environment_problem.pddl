(define (problem SliosEnvironmentProblem) (:domain SliosEnvironmentDomain)
(:objects o - outside r1 r2 r3 - room t1 t2 t3 t4 t5 t6 t7 t8 - table )(:init (presenceInRoom r1) (lowTemp r1) (midHum r1) (lightOn r1) (lowerOutsideTemp r2) (midTemp r2) (midHum r2) (lowLight r2) (climateOn r2) (lightOn r2) (lowerOutsideTemp r3) (midTemp r3) (midHum r3) (lowLight r3) (climateOn r3) (loudSound t1) (loudSound t2) (lowlightOutside o) ) (:goal (and (or (and 
                    (not(presenceInRoom r1)) 
                    (not(lightOn r1)) 
                    (weathersafe r1) 
                    (not(highCO2 r1)))
                (and
                    (presenceInRoom r1)
                    (midTemp r1)
                    (midHum r1)
                    (not(highCO2 r1))
                    ;(not(lowLight r1))
                    (efficient-light r1) 
                    (weathersafe r1))
            )
            (or (and 
                    (not(presenceInRoom r2)) 
                    (not(lightOn r2)) 
                    (weathersafe r2) 
                    (not(highCO2 r2)))
                (and
                    (presenceInRoom r2)
                    (midTemp r2)
                    (midHum r2)
                    (not(highCO2 r2))
                    ;(not(lowLight r2))
                    (efficient-light r2)  
                    (weathersafe r2)))
            (or (and 
                    (not(presenceInRoom r3)) 
                    (not(lightOn r3)) 
                    (weathersafe r3) 
                    (not(highCO2 r3)))
                (and
                    (presenceInRoom r3)
                    (midTemp r3)
                    (midHum r3)
                    (not(highCO2 r3))
                    ;(not(lowLight r3))
                    (efficient-light r3)  
                    (weathersafe r3)))
            (and(not (loudSound t1))
                (not (loudSound t2))
                (not (loudSound t3))
                (not (loudSound t4))
                (not (loudSound t5))
                (not (loudSound t6))
                (not (loudSound t7))
                (not (loudSound t8)))
)
)
)