(define (domain SliosDistributionDomain)

    (:requirements 
        :strips 
        :typing 
        :negative-preconditions
        :equality 
        :disjunctive-preconditions 
        :conditional-effects)

    (:types room person chair - object)

    (:predicates 
        (new-person ?p - person)
        (person-at ?p - person ?c - chair ?r - room) 
        (free-chair ?c - chair ?r - room)
        (one-more-person-in-room ?r - room)
        (two-more-person-in-room ?r - room)
        (three-more-person-in-room ?r - room)
    )
    

    (:action even-distributed-reset 
        :parameters (?r1 ?r2 ?r3 - room) 
        :precondition (and  (not(= ?r1 ?r2))
                            (not(= ?r1 ?r3))
                            (not(= ?r2 ?r3))
                            (or (one-more-person-in-room ?r1) (two-more-person-in-room ?r1) (three-more-person-in-room ?r1))
                            (or (one-more-person-in-room ?r2) (two-more-person-in-room ?r2) (three-more-person-in-room ?r2))
                            (or (one-more-person-in-room ?r3) (two-more-person-in-room ?r3) (three-more-person-in-room ?r3))) 
        :effect (and    (when (one-more-person-in-room ?r1) (not(one-more-person-in-room ?r1)))
                        (when (two-more-person-in-room ?r1) (and (not(two-more-person-in-room ?r1)) (one-more-person-in-room ?r1)))
                        (when (three-more-person-in-room ?r1) (and (not(three-more-person-in-room ?r1)) (two-more-person-in-room ?r1)))
                        (when (one-more-person-in-room ?r2) (not(one-more-person-in-room ?r2)))
                        (when (two-more-person-in-room ?r2) (and (not(two-more-person-in-room ?r2)) (one-more-person-in-room ?r2)))
                        (when (three-more-person-in-room ?r2) (and (not(three-more-person-in-room ?r2)) (two-more-person-in-room ?r2)))
                        (when (one-more-person-in-room ?r3) (not(one-more-person-in-room ?r3)))
                        (when (two-more-person-in-room ?r3) (and (not(two-more-person-in-room ?r3)) (one-more-person-in-room ?r3)))
                        (when (three-more-person-in-room ?r3) (and (not(three-more-person-in-room ?r3)) (two-more-person-in-room ?r3)))
    ))

    (:action place-person-on-chair 
        :parameters (?p - person ?r - room ?c - chair) 
        :precondition (and (new-person ?p) (free-chair ?c ?r)  (not(one-more-person-in-room ?r)) (not(two-more-person-in-room ?r)) (not(three-more-person-in-room ?r))) ;
        :effect (and (not(new-person ?p)) (not(free-chair ?c ?r)) (person-at ?p ?c ?r) (one-more-person-in-room ?r))
    )

    (:action reject-new-person-because-full
        :parameters (?p - person)
        :precondition (and (new-person ?p) (forall (?c - chair) (forall (?r - room) (not(free-chair ?c ?r)))))
        :effect (not(new-person ?p))
    )
)