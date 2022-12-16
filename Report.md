CSC1034 Report_220185181
====

### How I make code optimization
1. Make a local variable
2. Substitute for loops by dict
3. Utilize the Short Circuit of if Statement

- To measure code execution times: 
Using time() method which returns the time as a floating point number expressed in seconds.

#### 1. Make a local variable.
In page_rank.py function stochastic_page_rank()

Using args.repeats, args.steps - Calculation took 52.36 seconds.

    for j in range(args.repeats):
        current_node = random.choice(list(graph))
        for i in range(args.steps):
            current_node = random.choice(graph[current_node])
            if current_node not in graph:
                break
        hit_count[current_node] += 1 / args.repeats
    return hit_count


Using n_repetitions, n_steps - Calculation took 52.31 seconds.

    n_repetitions = args.repeats
    n_steps = args.steps

    for j in range(n_repetitions):
        current_node = random.choice(list(graph))
        for i in range(n_steps):
            current_node = random.choice(graph[current_node])
            if current_node not in graph:
                break
        hit_count[current_node] += 1 / n_repetitions
    return hit_count

To change variables, I created two local variables n_repetitions assign a value to args.repeats and n_steps assign a value to args.steps. Because using the local variable is faster than the global variable in 
the run time. When I ran each code, the speed of accessing args.repeats was slower than accessing n_repetitions.



#### 2. Substitute for loops by dict
In page_rank.py function stochastic_page_rank()
Making dictionary before using for loop - Calculation took 55.86 seconds.

    hit_count = dict()
    for node in graph:
        hit_count[node] = 0


Making dictionary and use for loop at once - Calculation took 55.81 seconds.  

    hit_count = { node:0 for node in graph }


When I initialized hit_count[node] with 0 for all nodes using for loop.
For loops are relatively slow so, I created a code to create a dictionary and executed it at once when
the for loop was executed once. When I ran the second code, the measurement results were slightly faster than the first code.



#### 3. Utilize the Short Circuit of if Statement
In page_rank.py function stochastic_page_rank()

Using if statement before simplification - Calculation took 52.61 seconds.

        if current_node in graph:
                continue
        else:
                break


Using simplified if statement - Calculation took 51.60 seconds.
    
    if current_node not in graph:
                break

In the repetition n_steps, chosen current_node is in the out edges of current_node. 
To check if the current_node is in graph while executing, at first I used the first code.
But when I was thinking about code, checking if the current_node is not in graph while executing and using break
is more effective because less checking to compare than first code.
So, I reduce the execution time by making a simplified if statement to run fewer times when checking for presence or absence. 


As a result, through three ways to make code optimizations, this program runtime in page_rank.py is reduced to 51.28 seconds.