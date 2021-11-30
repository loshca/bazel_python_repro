def impl(ctx):
    out = ctx.actions.declare_file("out.txt")
    ctx.actions.run(
        executable = ctx.executable._tool,
        outputs = [out]
    )

    return [
        DefaultInfo(files = depset([out]))
    ]

my_python_rule = rule(
    implementation = impl,
    attrs = {
        "_tool": attr.label(
            default=":tool",
            executable = True,
            cfg = "host",
        )
    }
)