import pytest

from stack_exchange.cache import Cache
from stack_exchange.models import Answer, Question, SearchRequest, SearchResult
from stack_exchange.search import Searchable


class TestCache(Cache):
    """In memory dict to simulate a cache"""

    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value


class TestStackExchangeClient(Searchable):
    def search(self, request: SearchRequest) -> list[SearchResult]:
        """Test search interface for stack-exchange"""
        questions = [
            Question(
                body="Question body 1",
                score=50,
                creation_date=1,
                title="Question title 1",
                link="stackexchange.com/1",
                accepted_answer_id=1,
            ),
            Question(
                body="Question body 2",
                score=10,
                creation_date=2,
                title="Question title 2",
                link="stackexchange.com/2",
                accepted_answer_id=2,
            ),
        ]
        answers = [
            Answer(body="Answer for question 1", score=100, creation_date=1, is_accepted=True, answer_id=1),
            Answer(body="Answer for question ", score=200, creation_date=2, is_accepted=True, answer_id=2),
        ]
        return [SearchResult(question, answer) for (question, answer) in zip(questions, answers)]


class TestCachedStackExchangeClient:
    def __init__(self):
        self.cache = Cache()
        self.service = TestStackExchangeClient()

    def search(self, request: SearchRequest) -> list[SearchResult]:
        request_url = "cached_url_key"
        cached_search_results = self.cache.get(request_url)

        if cached_search_results is not None:
            return [SearchResult.from_json(sr_json) for sr_json in cached_search_results]

        search_results = self.service.search(request)
        search_results_json = [sr.to_json() for sr in search_results]

        self.cache.set(key=request_url, value=search_results_json)

        return search_results


@pytest.fixture
def search_request():
    request = (
        SearchRequest.Builder("Reverse a linked-list", "stackoverflow")
        .with_tags("python")
        .accepted_only()
        .n_results(10)
        .build()
    )
    return request


@pytest.fixture
def stack_exchange():
    return TestStackExchangeClient()


@pytest.fixture()
def cached_stack_exchange():
    return TestCachedStackExchangeClient()


@pytest.fixture
def cache():
    return TestCache()


@pytest.fixture
def error_stack_exchange_http_response():
    return {"error_id": 502, "error_message": "too many requests from this IP", "error_name": "throttle_violation"}


@pytest.fixture
def stack_search_response():
    return {
        "items": [
            {
                "tags": ["algorithm", "graph-algorithm", "graph-theory", "depth-first-search", "breadth-first-search"],
                "owner": {
                    "account_id": 635364,
                    "reputation": 4489,
                    "user_id": 394924,
                    "user_type": "unregistered",
                    "profile_image": "https://www.gravatar.com/avatar/c80fef37e983496292ff2724d0ecf96d?s=256&d=identicon&r=PG",
                    "display_name": "Parth",
                    "link": "https://stackoverflow.com/users/394924/parth",
                },
                "is_answered": True,
                "view_count": 331915,
                "protected_date": 1591311777,
                "closed_date": 1591385804,
                "accepted_answer_id": 3332994,
                "answer_count": 15,
                "score": 440,
                "last_activity_date": 1638391388,
                "creation_date": 1280129043,
                "last_edit_date": 1520795891,
                "question_id": 3332947,
                "link": "https://stackoverflow.com/questions/3332947/when-is-it-practical-to-use-depth-first-search-dfs-vs-breadth-first-search-bf",
                "closed_reason": "Opinion-based",
                "title": "When is it practical to use Depth-First Search (DFS) vs Breadth-First Search (BFS)?",
                "body": "<p>I understand the differences between DFS and BFS, but I'm interested to know when it's more practical to use one over the other? </p>\n\n<p>Could anyone give any examples of how DFS would trump BFS and vice versa?</p>\n",
            },
            {
                "tags": ["graph", "graph-theory"],
                "owner": {
                    "account_id": 102773,
                    "reputation": 6534,
                    "user_id": 275674,
                    "user_type": "registered",
                    "accept_rate": 62,
                    "profile_image": "https://www.gravatar.com/avatar/c5b3720a75b29cab2a8f1c8162a19f27?s=256&d=identicon&r=PG",
                    "display_name": "Jony",
                    "link": "https://stackoverflow.com/users/275674/jony",
                },
                "is_answered": True,
                "view_count": 77356,
                "protected_date": 1608045160,
                "closed_date": 1608045675,
                "accepted_answer_id": 2626251,
                "answer_count": 4,
                "score": 68,
                "last_activity_date": 1608045538,
                "creation_date": 1271116852,
                "last_edit_date": 1271117081,
                "question_id": 2626198,
                "link": "https://stackoverflow.com/questions/2626198/graphs-data-structure-dfs-vs-bfs",
                "closed_reason": "Opinion-based",
                "title": "Graphs data structure: DFS vs BFS?",
                "body": "<p>if given a graph problem how do we know whether we need to use bfs or dfs algorithm???\nor when do we use dfs algorithm or bfs algorithm.\nWhat are the differences and advantages of one over other?</p>\n",
            },
            {
                "tags": ["data-structures", "graph-theory", "depth-first-search", "breadth-first-search"],
                "owner": {
                    "account_id": 9091106,
                    "reputation": 310,
                    "user_id": 8564970,
                    "user_type": "registered",
                    "profile_image": "https://graph.facebook.com/613863685448920/picture?type=large",
                    "display_name": "Shreyas Pimpalgaonkar",
                    "link": "https://stackoverflow.com/users/8564970/shreyas-pimpalgaonkar",
                },
                "is_answered": True,
                "view_count": 9817,
                "accepted_answer_id": 47225097,
                "answer_count": 1,
                "score": 9,
                "last_activity_date": 1609162594,
                "creation_date": 1510317069,
                "last_edit_date": 1542680960,
                "question_id": 47222855,
                "content_license": "CC BY-SA 4.0",
                "link": "https://stackoverflow.com/questions/47222855/in-what-sense-is-dfs-faster-than-bfs",
                "title": "In what sense is DFS faster than BFS?",
                "body": "<p>While reading about DFS vs BFS, I came across a statement that DFS is faster than BFS, and requires less memory.</p>\n\n<p>My implementation is in C++ for both, making a stack for DFS and queue for BFS. Can someone please explain what, and how are the speed and memory requirements different?</p>\n",
            },
            {
                "tags": ["web-crawler", "webpage", "depth-first-search"],
                "owner": {
                    "account_id": 2435761,
                    "reputation": 171,
                    "user_id": 2125709,
                    "user_type": "registered",
                    "accept_rate": 33,
                    "profile_image": "https://www.gravatar.com/avatar/68db3df7b9e483cf3f088d18bf8633e0?s=256&d=identicon&r=PG",
                    "display_name": "Nazgol",
                    "link": "https://stackoverflow.com/users/2125709/nazgol",
                },
                "is_answered": True,
                "view_count": 8979,
                "closed_date": 1387010947,
                "accepted_answer_id": 20580936,
                "answer_count": 1,
                "score": 6,
                "last_activity_date": 1489167093,
                "creation_date": 1386989652,
                "last_edit_date": 1489167093,
                "question_id": 20579169,
                "link": "https://stackoverflow.com/questions/20579169/dfs-vs-bfs-in-web-crawler-design",
                "closed_reason": "Needs more focus",
                "title": "DFS vs BFS in web crawler design",
                "body": "<p>I come up with an interview question that I would like to know your opinion about that. The questions are say that in designing a web crawler:</p>\n\n<p>1) what kind of pages will you hit with a DFS versus BFS?</p>\n\n<p>2) how would you avoid getting into infinite loops?</p>\n\n<p>I appreciate if somebody could answer them.</p>\n",
            },
            {
                "tags": ["algorithm", "graph", "breadth-first-search", "depth-first-search"],
                "owner": {
                    "account_id": 5974026,
                    "reputation": 313,
                    "user_id": 4695532,
                    "user_type": "registered",
                    "accept_rate": 37,
                    "profile_image": "https://www.gravatar.com/avatar/748864988b8028510b8322569a1668ea?s=256&d=identicon&r=PG&f=1",
                    "display_name": "sb15",
                    "link": "https://stackoverflow.com/users/4695532/sb15",
                },
                "is_answered": True,
                "view_count": 1088,
                "accepted_answer_id": 33423404,
                "answer_count": 1,
                "score": 3,
                "last_activity_date": 1485611691,
                "creation_date": 1446136088,
                "last_edit_date": 1485611691,
                "question_id": 33419712,
                "content_license": "CC BY-SA 3.0",
                "link": "https://stackoverflow.com/questions/33419712/dfs-vs-bfs-confusion",
                "title": "Dfs Vs Bfs confusion",
                "body": '<p>From a <a href="https://www.topcoder.com/community/data-science/data-science-tutorials/introduction-to-graphs-and-their-data-structures-section-2/" rel="nofollow">topcoder article</a>:</p>\n\n<blockquote>\n  <p>"In BFS We mark a vertex visited as we push it into the queue, not as\n  we pop it in case of DFS."</p>\n</blockquote>\n\n<p><strong>NOTE:</strong> This is said in case of dfs implementation using explicit stack.(pseudo dfs).</p>\n\n<p>My question is why so? why we can not mark a vertex visited after popping from queue, instead while pushing onto the queue in case of bfs ?</p>\n',
            },
            {
                "tags": ["algorithm", "time-complexity", "depth-first-search", "breadth-first-search", "pseudocode"],
                "owner": {
                    "account_id": 21591583,
                    "reputation": 25,
                    "user_id": 15921100,
                    "user_type": "registered",
                    "profile_image": "https://www.gravatar.com/avatar/d7e4615a44045967d621222a75adef05?s=256&d=identicon&r=PG&f=1",
                    "display_name": "George Walter",
                    "link": "https://stackoverflow.com/users/15921100/george-walter",
                },
                "is_answered": True,
                "view_count": 811,
                "accepted_answer_id": 67531003,
                "answer_count": 1,
                "score": 2,
                "last_activity_date": 1620981085,
                "creation_date": 1620961050,
                "question_id": 67528549,
                "content_license": "CC BY-SA 4.0",
                "link": "https://stackoverflow.com/questions/67528549/depth-first-search-dfs-vs-breadth-first-search-bfs-pseudocode-and-complexity",
                "title": "Depth first search (DFS) vs breadth first search (BFS) pseudocode and complexity",
                "body": "<p>I have to develop pseudocode for an algorithm that computes the number of connected\ncomponents in a graph G = (V, E) given vertices V and edges E.</p>\n<p>I know that I can use either depth-first search or breadth-first search to calculate the number of connected components.</p>\n<p>However, I want to use the most efficient algorithm to solve this problem, but I am unsure of the complexity of each algorithm.</p>\n<p>Below is an attempt at writing DFS in pseudocode form.</p>\n<pre><code>function DFS((V,E))\n     mark each node in V with 0\n     count ← 0\n     for each vertex in V do\n          if vertex is marked then\n               DFSExplore(vertex)\n\nfunction DFSExplore(vertex)\n     count ← count + 1\n     mark vertex with count\n     for each edge (vertex, neighbour) do\n          if neighbour is marked with 0 then\n               DFSExplore(neighbour)\n</code></pre>\n<p>Below is an attempt at writing BFS in pseudocode form.</p>\n<pre><code>function BFS((V, E))\n     mark each node in V with 0\n     count ← 0, init(queue)     #create empty queue \n     for each vertex in V do\n          if vertex is marked 0 then\n               count ← count + 1\n               mark vertex with count\n               inject(queue, vertex)             #queue containing just vertex\n               while queue is non-empty do\n                    u ← eject(queue)                          #dequeues u\n                    for each edge (u, w) adjacent to u do\n                         if w is marked with 0 then\n                              count ← count + 1\n                              mark w with count\n                              inject(queue, w)     #enqueues w\n</code></pre>\n<p>My lecturer said that BFS has the same complexity as DFS.</p>\n<p>However, when I searched up the complexity of depth-first search it was O(V^2), while the complexity of breadth-first search is O(V + E) when adjacency list is used and O(V^2) when adjacency matrix is used.</p>\n<p>I want to know how to calculate the complexity of DFS / BFS and I want to know how I can adapt the pseudocode to solve the problem.</p>\n",
            },
            {
                "tags": ["algorithm", "search", "recursion", "depth-first-search"],
                "owner": {
                    "account_id": 3397275,
                    "reputation": 3327,
                    "user_id": 2850548,
                    "user_type": "registered",
                    "accept_rate": 78,
                    "profile_image": "https://i.stack.imgur.com/v7L6r.png?s=256&g=1",
                    "display_name": "FuzzyBunnySlippers",
                    "link": "https://stackoverflow.com/users/2850548/fuzzybunnyslippers",
                },
                "is_answered": True,
                "view_count": 1610,
                "accepted_answer_id": 20500817,
                "answer_count": 1,
                "score": 1,
                "last_activity_date": 1386695412,
                "creation_date": 1386684471,
                "last_edit_date": 1495540357,
                "question_id": 20496659,
                "content_license": "CC BY-SA 3.0",
                "link": "https://stackoverflow.com/questions/20496659/is-classical-recursion-based-depth-first-search-more-memory-efficient-than-sta",
                "title": "Is classical (recursion based) depth first search more memory efficient than stack based DFS?",
                "body": '<p>I was looking at the responses to <a href="https://stackoverflow.com/questions/20429310/why-is-dfs-depth-first-search-claimed-to-be-space-efficient/20429438#20429438">this</a> question by @AndreyT and I had a question regarding the memory efficiency of classical DFS vs. stack based DFS.  The argument is that the classical backtracking DFS cannot be created from BFS by a simple stack-to-queue replacement.  In doing the BFS to DFS by stack-to-queue replacement, you lose the space efficiency of classical DFS.  Not being a search algorithm expert (though I am reading up on it)  I\'m going to assume this is just "true" and go with it.</p>\n\n<p>However, my question is really about overall memory efficiency.  While a recursive solution does have a certain code efficiency (I can do a lot more with a few lines of recursive search code) and elegance, doesn\'t it have a memory (and possibly performance) "hit" because of the fact it is recursive?  </p>\n\n<p>Every time you recurse into the function, it pushes local data onto the stack, the return address of the function, and whatever else the compiler thought was necessary to maintain state on return, etc.  This can add up quickly.  It also has to make a function call for each recursion, which eats up some ops as well (maybe minor...or maybe it breaks branching predictability forcing a flush of the pipeline...not an expert here...feel free to chime in).  </p>\n\n<p>I think I want to stick to simple recursion for now and not get into "alternative forms" like tail-recursion for the answer to this question.  At least for now.</p>\n',
            },
            {
                "tags": ["algorithm", "graph-algorithm"],
                "owner": {
                    "account_id": 14310578,
                    "reputation": 175,
                    "user_id": 10336980,
                    "user_type": "registered",
                    "profile_image": "https://www.gravatar.com/avatar/bd91b41ff2f48e50aaee97bbe37f5e13?s=256&d=identicon&r=PG&f=1",
                    "display_name": "terrabyte",
                    "link": "https://stackoverflow.com/users/10336980/terrabyte",
                },
                "is_answered": True,
                "view_count": 136,
                "accepted_answer_id": 70198010,
                "answer_count": 2,
                "score": 1,
                "last_activity_date": 1639176620,
                "creation_date": 1638438040,
                "question_id": 70197120,
                "content_license": "CC BY-SA 4.0",
                "link": "https://stackoverflow.com/questions/70197120/infinite-nodes-in-bfs-vs-dfs",
                "title": "Infinite nodes in BFS vs DFS",
                "body": "<p>People always talk about how if there are infinite nodes downwards, then DFS will get stuck traversing this infinitely long branch and never reaching the answer in another branch.</p>\n<p>Isn't this applicable to BFS as well? For example if the root node has an infinite amount of neighbours, wouldn't the program just spend an infinite amount of time trying to add each one into a queue?</p>\n",
            },
            {
                "tags": ["multithreading", "process", "operating-system", "locks"],
                "owner": {
                    "account_id": 13114418,
                    "reputation": 156,
                    "user_id": 9474172,
                    "user_type": "registered",
                    "profile_image": "https://i.stack.imgur.com/7lpIp.jpg?s=256&g=1",
                    "display_name": "Piyush Sawarkar",
                    "link": "https://stackoverflow.com/users/9474172/piyush-sawarkar",
                },
                "is_answered": True,
                "view_count": 421,
                "accepted_answer_id": 61791619,
                "answer_count": 3,
                "score": 0,
                "last_activity_date": 1589443547,
                "creation_date": 1589353367,
                "last_edit_date": 1589353667,
                "question_id": 61768299,
                "content_license": "CC BY-SA 4.0",
                "link": "https://stackoverflow.com/questions/61768299/can-a-single-process-thread-ever-cause-deadlock",
                "title": "Can a single Process / Thread ever cause deadlock?",
                "body": "<p>I was reading concept of deadlock from Galvin and I am getting a doubt that can a single process / thread ever go in deadlock...?\nCoz the definition (or as a matter of fact the whole Deadlock chapter in Galvin) doesnt seem to be talking about what if there is a single process / thread in the system..\n(Plz tell if I have missed upon any point..while reading it...if yes sincere apology..for my previous statement but I simply could not find it in chapter anywhere..)</p>\n\n<p>Every where Galvin Book uses the word \"Other\" process while describing deadlock scenario...\nSo what I feel the answer to my question is No , a single process / thread can never go in deadlock..\n(Okay also me: what I feel that a single process in some case may lead to indefinite waiting ..can I call it as a deadlock..?)</p>\n\n<p>To know the motivation why I am bringing Deadlock and Indefinite waiting into one Picture..plz read below scenario\n(Okay also plz let me know that whether I am correct in assuming that indefinite waiting is not same as deadlock...i may be wrong..??)\nConsider a scenario:\nThere is one thread (t) and one lock(l).\nLock nature Non re entrant.\n(Meaning when thread holds lock l then it cannot acquire it once again before it releases it...I could find only this as definition on internet.)\n(One more condition:\nIf a thread could not acquire lock then it blocks itself untill it gets available...yes it's pretty obvious point but this point is creating mess..plz read below to get insight..)\nNow it's claimed that say t acquires a lock l and then does its execution meanwhile it requires the same lock again..(may be because it has to Do some recursive function call...like as in BFS/ DFS...or may be something similar..)\nSo obviously it has to leave that lock before acquiring that lock...but since process cannot acquire same lock again so it has to wait or simply gets blocked till it becomes available...\nNow the important point is ...it would be blocked till it ..itself releases the lock..now my question is can this scenario lead to a deadlock...\n(Yes it can release again..and then reacquire...but my problem is not pertaining to this case..)\nSo my problem is can this case ever lead to deadlock...(like thread waits for itself...)\n-->like in worst case type scenario..\n(Also whenever a process / thread  goes in blocking state /waiting state does it hold locks/ resources..??plz also shed light here ...)\n(I hope what I am talking about is clear...if not plz comment and tell I'll try my best to clarify...yes this point is very delicate where I want to raise doubt)</p>\n\n<p>That scenario is actually an exam problem..whose answer is : Yes a single thread with single lock can lead to deadlock-->which I feel conflicts with deadlock defintion..)\nI know I am raising many doubts but the primary problem is same.</p>\n\n<p>Below is key point summary of my doubt:</p>\n\n<p>-single process/ there's in deadlock?</p>\n\n<p>-indefinite wait vs deadlock</p>\n\n<p>-is it necessary for a process/thread to release locks..when goes in blocked/waiting state?</p>\n\n<p>(First of all thanks if you made it till this point...coz it's really a long doubt..I did it just so as to make my point clear...if not comment..I'll make it again..)</p>\n",
            },
            {
                "tags": ["c++", "oop", "graph", "breadth-first-search"],
                "owner": {
                    "account_id": 23340995,
                    "reputation": 5,
                    "user_id": 18480976,
                    "user_type": "registered",
                    "profile_image": "https://lh3.googleusercontent.com/a/AATXAJwCdcHjBaEYnCcKWF-ra4ucD5Jkm9ouxYlsXbFP=k-s256",
                    "display_name": "Ayush Agarwal ",
                    "link": "https://stackoverflow.com/users/18480976/ayush-agarwal",
                },
                "is_answered": True,
                "view_count": 38,
                "accepted_answer_id": 72575772,
                "answer_count": 1,
                "score": 0,
                "last_activity_date": 1655028752,
                "creation_date": 1654860017,
                "last_edit_date": 1655028752,
                "question_id": 72573454,
                "content_license": "CC BY-SA 4.0",
                "link": "https://stackoverflow.com/questions/72573454/grid-graph-path-finder-code-using-bfs-in-c",
                "title": "Grid-graph path finder code using BFS in c++",
                "body": '<p>I\'m trying to code BFS algorithm in C++ for finding a cell in a grid , however the code is not giving any output (just blank ) . The code is similar to all standard codes given online but I am unable to understand how it is not working .</p>\n<p>class grid graph is the class to declare the graph , which is a 2d array , with 0 as path and 1 as obstacle</p>\n<p>pathfinder is a method to find the path , using breadth first search algorithm\nand it has its own helper function add neighbours to add neighbours</p>\n<pre><code>#include&lt;iostream&gt;\n#include &lt;bits/stdc++.h&gt;\nusing namespace std ;\nclass grid_graph{\n    public:\n    vector&lt;vector&lt;int&gt;&gt; A;\n    grid_graph(vector&lt;vector&lt;int&gt;&gt; a){\n        A = a;\n    }\n    int N_rows = A.size();\n    int N_cols = A[0].size();\n    \n    void pathfinder(int src_r,int src_c,int dest_r,int dest_c);\n    void neighbour_adder(int r,int c,queue&lt;int&gt;&amp; R,queue&lt;int&gt;&amp; C,vector&lt;vector&lt;bool&gt;&gt;&amp; visited);//bool visited[][N_cols]\n};\nvoid grid_graph::pathfinder(int src_r,int src_c,int dest_r,int dest_c){\n    queue&lt;int&gt; R;\n    queue&lt;int&gt; C;\n    R.push(src_r);\n    C.push(src_c);\n    // bool visited[N_rows][N_cols]{};\n    vector&lt;vector&lt;bool&gt;&gt; visited;\n    for(int i=0; i&lt;N_rows; i++){\n        for(int j=0; j&lt;N_cols; j++){\n            visited[i][j]=false;\n        }\n    }\n    // visited[src_r][src_c] = true;\n    while(!R.empty()){\n        cout&lt;&lt;R.front()&lt;&lt;&quot; &quot;&lt;&lt;C.front()&lt;&lt;endl;\n        if(R.front()==dest_r &amp;&amp; C.front()==dest_c){\n            cout&lt;&lt;&quot;reached&quot;&lt;&lt;endl;\n        }\n        visited[R.front()][C.front()]=true;\n        neighbour_adder(R.front(),C.front(),R,C,visited);\n        R.pop();\n        C.pop();\n    }\n}\nvoid grid_graph::neighbour_adder(int r,int c,queue&lt;int&gt;&amp; R,queue&lt;int&gt;&amp; C,vector&lt;vector&lt;bool&gt;&gt;&amp; visited){//bool visited[][N_cols]\n    // assuming only up down left right motion possible \n    int d1[4] = {0,0,+1,-1};\n    int d2[4] = {+1,-1,0,0};\n    for(int i=0; i&lt;4; i++){\n        int r_next = r + d1[i];\n        int c_next = c + d2[i];\n        if(r_next&lt;0 || c_next&lt;0 || r_next&gt;=N_rows || c_next&gt;=N_cols){\n            continue;\n        }\n        // I have taken 1 as obstacle 0 as not obstacle \n        if(A[r_next][c_next]==1 || visited[r_next][c_next]==true){\n            continue;\n        }\n        R.push(r_next);\n        C.push(c_next);\n    }\n\n}\n\nint main(){\n    \n    grid_graph g2( {{ 0, 0, 0 },\n                    { 0, 1, 0 },\n                    { 0, 0, 0 } });\n    g2.pathfinder(0,0,2,2);\n    return 0;\n}\n</code></pre>\n<p>EDIT 1 : The code now perfectly works thanks to the solution , here is the working code for anyone else who needs it :</p>\n<p>/</p>\n<pre><code>/////////////////////////////////////////////////\nclass grid_graph{\n    public:\n    vector&lt;vector&lt;int&gt;&gt; A;\n    // grid_graph(vector&lt;vector&lt;int&gt;&gt; a){\n    //     A = a;\n    // }\n    // int N_rows = A.size();\n    // int N_cols = A[0].size();\n    /////////////////////////////////////////////////////////////// from SO\n    grid_graph(vector&lt;vector&lt;int&gt;&gt; a): A( a ){}\n\n    int colCount() const\n    {\n        return A[0].size();\n    }\n    int rowCount() const\n    {\n        return A.size();\n    }\n    ////////////////////////////////////////////////////////////\n    void pathfinder(int src_r,int src_c,int dest_r,int dest_c);\n    void neighbour_adder(int r,int c,queue&lt;int&gt;&amp; R,queue&lt;int&gt;&amp; C,vector&lt;vector&lt;bool&gt;&gt;&amp; visited);//bool visited[][N_cols]\n};\nvoid grid_graph::pathfinder(int src_r,int src_c,int dest_r,int dest_c){\n    queue&lt;int&gt; R;\n    queue&lt;int&gt; C;\n    R.push(src_r);\n    C.push(src_c);\n    // bool visited[N_rows][N_cols]{};\n    // vector&lt;vector&lt;bool&gt;&gt; visited;\n    // for(int i=0; i&lt;N_rows; i++){\n    //     for(int j=0; j&lt;N_cols; j++){\n    //         visited[i][j]=false;\n    //     }\n    // }\n    int N_rows = rowCount();\n    int N_cols = colCount();\n    ///////////////////////////////////from stackexchange \n    vector&lt;vector&lt;bool&gt; &gt; visited(N_rows,vector&lt;bool&gt;(N_cols, false));\n    /////////////////////////////////\n    // visited[src_r][src_c] = true;\n    while(!R.empty()){\n        if(R.front()==dest_r &amp;&amp; C.front()==dest_c){\n            cout&lt;&lt;&quot;reached&quot;&lt;&lt;endl;\n        }\n        visited[R.front()][C.front()]=true;\n        neighbour_adder(R.front(),C.front(),R,C,visited);\n        R.pop();\n        C.pop();\n    }\n}\nvoid grid_graph::neighbour_adder(int r,int c,queue&lt;int&gt;&amp; R,queue&lt;int&gt;&amp; C,vector&lt;vector&lt;bool&gt;&gt;&amp; visited){//bool visited[][N_cols]\n    // assuming only up down left right motion possible \n    int d1[4] = {0,0,+1,-1};\n    int d2[4] = {+1,-1,0,0};\n    int N_rows = rowCount();\n    int N_cols = colCount();\n    for(int i=0; i&lt;4; i++){\n        int r_next = r + d1[i];\n        int c_next = c + d2[i];\n        if(r_next&lt;0 || c_next&lt;0 || r_next&gt;=N_rows || c_next&gt;=N_cols){\n            continue;\n        }\n        // I have taken 1 as obstacle 0 as not obstacle \n        if(A[r_next][c_next]==1 || visited[r_next][c_next]==true){\n            continue;\n        }\n        R.push(r_next);\n        C.push(c_next);\n    }\n\n}\n/////////////////////////////////////////////////////////////////////////////////////////////////\n/* Dijkstra algorithm is a greedy algorithm used for shortest path in non negative weighted\n graphs . we have lazy , eager , d ary heap and fibonacci heap versions of it . \n*/\n/*Topological sort , topsort done using dfs over all unvisited nodes and putting them in reverse \nin an array (which is the topsort output ) , can only be done over directed acyclic graph  DAG*/\nint main(){\n    // cout&lt;&lt;&quot;hello world&quot;&lt;&lt;endl;\n    unweighted_graph g1;\n    /////////////////////////////////////\n    // g1.addedge_undirected(1,2);\n    // g1.addedge_directed(2,3);\n    // g1.print_graph();\n    // print graph , directed and undirected edges functions are working properly \n    ////////////////////////////////////\n\n    ////////////////////////////////////\n    // graph taken from https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/\n    // g1.addedge_directed(0, 1);\n    // g1.addedge_directed(0, 2);\n    // g1.addedge_directed(1, 2);\n    // g1.addedge_directed(2, 0);\n    // g1.addedge_directed(2, 3);\n    // g1.addedge_directed(3, 3);\n    // g1.BFS_iterative(2);\n    // gave output 2 0 3 1 which is correct hence iterative BFS is working properly \n    // g1.BFS_recursive(2);\n    // gave output 2 0 3 1 which is correct hence recursive BFS is working correctly \n    ////////////////////////////////////\n    // g.addedge_directed(0, 1);\n    // g.addedge_directed(0, 2);\n    // g.addedge_directed(1, 2);\n    // g.addedge_directed(2, 0);\n    // g.addedge_directed(2, 3);\n    // g.addedge_directed(3, 3);\n    // g.DFS_iterative(0);\n    // gave output 2 3 0 1 for 2 , 3 for 3 , 0 2 3 1 for 0 hence it is working \n    // g.DFS_recursive(0);\n    // gave output 2 0 1 3 for 2 , 3 for 3 , 0 1 2 3 for 0 hence it is working \n    ////////////////////////////////////\n    grid_graph g2( {{ 0, 0, 0 },\n                    { 0, 1, 0 },\n                    { 0, 0, 0 } });\n    g2.pathfinder(0,0,2,2);\n\n    return 0;\n}\n</code></pre>\n<p>My VS Code is showing bits/std.h not found error , and I have no idea where the libraries are on my pc and how to source , so can anyone help in it too</p>\n<p>EDIT 2 - Code is now availaible at github along with code for BFS DFS Dijkstra at <a href="https://github.com/ayush-agarwal-0502/Graph-Algorithms-" rel="nofollow noreferrer">https://github.com/ayush-agarwal-0502/Graph-Algorithms-</a></p>\n',
            },
        ],
        "has_more": False,
        "quota_max": 300,
        "quota_remaining": 297,
    }
