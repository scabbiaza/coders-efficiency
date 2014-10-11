# Coders' efficiency rating

Script create coders' efficiency rating by analyse git repository data.<br/> 
*Commercial projects oriented.*

## Example

<pre>
Author         LOC total     Working days        Contribution     Efficiency

Coder 1            10362              124              33.79%            4.5
Coder 2             9655              130              31.49%            4.0
Coder 3             1250               28               4.08%            2.4
Coder 4             2364               55               7.71%            2.3
Coder 5             1403               55               4.58%            1.4
Coder 6              177                9               0.58%            1.1
Coder 7             1864              100               6.08%            1.0
</pre>


## How it works

#### What is coder's efficiency?
 
Is it how many lines he adds? But if developer added to the project some outer library (jQuery for example), should it count? Or if other developer rewrote that code because it was not correct, should it count? So may be efficiency is how many lines he deletes? Even more confusing metric, right? How many commits he creates? Well, it's important but...
 
The only thing that is really important is the **сode in release repository**.
That code has survived and we can call it **effective**.

**Coder's efficiency** is how much effective code he produced compared to other team members.

 
#### Example
 
Team created a project in 100 working days and the final repo has 10'000 LOC. 
 
John worked on this project from the beginning up to the end and created 5000 LOC for release repo. His contribution in release repo is:<br/>
```10'000 total LOC / 5000 author LOC = 50%```

Potential LOC for project that John could create is:<br/>
```(5000 author LOC / 100 working days) * 100 working days = 5000 LOC```

Peter worked on the project only 50 days and created 3000 LOC. His contribution is:<br/>
```10'000 total LOC / 3000 author LOC = 30%```

Potential LOC for project that Peter could create is:<br/>
```(3000 author LOC / 50 working days) * 100 working days = 6000 LOC```

And Mark worked on the project 80 days and created 2000 LOC. His part of contribution is:<br/>
```10'000 total LOC / 2000 author LOC = 20%```

Potential LOC for project that Mark could create is:<br/>
```(2000 author LOC / 80 working days) * 100 working days = 2500 LOC```


Efficiency for every member we will count as:<br/>
```potential LOC / min potential LOC```

 
**Members' Efficiency Statistic would be next**

<pre>
Author         LOC total     Working days        Contribution     Efficiency

Peter               3000               50                 30%            2.4
John                5000              100                 50%            2.0
Mark                2000               80                 20%            1.0
</pre>


You can see, that contribution and total LOC don't have direct relationship with Coder's Efficiency.
Still for the project all metrics are import.
 

### Important notices
 
* This statistic will have sense only if you analyze release repo. Code should be stable.
* This script will show you correct results if working day for every coders is the same, for example 8&nbsp;hours per day. That is why script marked as *commercial oriented*. 
* Any day coder has added commits is count as working day.
* It's only CODERS' rating. Keep in mind that developers do the other stuff as well: review the code, write documentation and so on. It will not count in this rating and here is why this script was named *Coders' efficiency* and not the *Developers' Efficiency*.



## Inspired by

* [GitInspector](https://code.google.com/p/gitinspector/)
* [GitStats](http://gitstats.sourceforge.net/)
* [GitFame](https://github.com/oleander/git-fame-rb)


## Contribution

If you want to contribute to the project, this links could be useful for you:

* [Git-log documentation](http://git-scm.com/docs/git-log)
* [Working with pythonsubprocess](http://jimmyg.org/blog/2009/working-with-python-subprocess.html)
