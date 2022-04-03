# Route-Table-Diff

This tool was born out of a need to compare routing tables and to easily identify any changes.  For small networks, home labs, etc. it's a trivial task to do so from the command line.  But for larger networks and for devices such as the Cisco Nexus 7k/9k which can contain hundreds if not thousands of routes it presents a bit more of a challenge.

Yes, there are *other* tools out there that do this better, but at the time were not available for use in this particular project. Therefore this *roll your own* tool was developed.

I have, for obvious reasons, had to sanitize the codebase because it is used in a production environment.  Before you faint at that thought, it was tested in my home lab and tested using static, but real world data to, as much as possible, ensure there were no *complications*.  That said, my goal in putting this on GitHub is to put it out there for review.  This is one of the more complicated things I have had to do with Python and I'd very much like to take the opportunity to learn.

I am looking for ways to just do it better.  Not with a more fitting tool, but with this approach.  Particularly making the code more efficient, more dynamic, more universal so that I could potentially use most of the code as a drop in for any other such efforts.  If you have a mind to mentoring a Python ameteur in a constructive manner (though I can take criticism if the code/situation calls for it, so don't be afraid), then please, reach out to me.
