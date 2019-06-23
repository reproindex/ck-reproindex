[![compatibility](https://github.com/ctuning/ck-guide-images/blob/master/ck-compatible.svg)](https://github.com/ctuning/ck)

Data license: [![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by/4.0/)
Code license: [![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Compatibility: Linux, MacOS, Windows


# Description

This repository contains reusable and cross-linked research components from reproduced papers in the [CK format](https://cKnowledge.org).

# Installation

Install CK as described [here](https://github.com/ctuning/ck#installation).

Create a fork of this repository at GitHub to be able to send PRs.

Pull the forked repository via CK:


```
$ ck pull repo:ck-reproindex --url={URL of the forked repository}
```

# Adding new article with reusable research

```
$ ck add repro.article
```

Answer ~12 questions about the article (you can just press Enter when a question is not applicable).
You can also find related answers in meta.json files of [already shared articles](https://github.com/reproindex/ck-reproindex/tree/master/repro.article).
You can use an [existing event tag](https://github.com/reproindex/ck-reproindex/blob/master/cfg/component/.cm/meta.json#L9)
or add a new one there.

CK will then create a new entry with the article meta description. You can commit your changes to your forked repo as follows:

```
$ ck find repo:ck-reproindex
$ cd `ck find repo:ck-reproindex`
$ git commit
$ git push
```

You can now create a PR for this repository. We will then review and update it if needed. 
When accepted, we will update this repository at reuseresearch.com to make your changes
available to the community in a user-friendly way.

# Updating reusable research components

Feel free to update meta description of other components and send us a PR:
* CK modules: [Web](http://reuseresearch.com/c.php?c=module) , [GitHub](https://github.com/reproindex/ck-reproindex/tree/master/component.module)
* CK repositories: [Web](http://reuseresearch.com/c.php?c=repo) , [GitHub](https://github.com/reproindex/ck-reproindex/tree/master/component.repo)
* CK software detection plugins: [Web](http://reuseresearch.com/c.php?c=soft) , [GitHub](https://github.com/reproindex/ck-reproindex/tree/master/component.soft)
* CK packages: [Web](http://reuseresearch.com/c.php?c=package) , [GitHub](https://github.com/reproindex/ck-reproindex/tree/master/component.package)
* CK tasks (program workflows): [Program](http://reuseresearch.com/c.php?c=program) , [GitHub](https://github.com/reproindex/ck-reproindex/tree/master/component.program)

# Indexing new CK components:

You can index new CK components as follows:

* CK modules: `ck index component.module:{CK module name} --share`
* CK repositories: `ck index component.repo:{CK repo name} --share`
* CK software detection plugins: `ck index component.soft:{CK soft name} --share`
* CK packages: `ck index component.package:{CK package name} --share`
* CK tasks (program workflows): `ck index component.program:{CK program name} --share`

You can then commit your changes and send us a PR as described above:
```
$ ck find repo:ck-reproindex
$ cd `ck find repo:ck-reproindex`
$ git commit
$ git push
```

# Notes

How to customize URL:

* https://reproindex.com/event/repro-asplos2020
* https://reproindex.com/papers&a=papers-ppopp-2019


# Feedback

This community project is in very early stage and there is still a lot to be done.
We need your participation and feedback to improve our open-source technology
and make it more convenient for researchers and engineers.
Please submit your issues and request features at https://github.com/reproindex/ck-reproindex/issues .

Feel free to register at the [ReproIndex website](https://reproindex.com/create-account) 
and sign up to our [twitter](https://twitter.com/ReproIndex) to keep track of the latest news. 
You are also very welcome to participate in this standardization effort 
via our [Slack channel](https://bit.ly/ck-slack) and 
this [public discussion group](https://groups.google.com/forum/#!forum/collective-knowledge). 
