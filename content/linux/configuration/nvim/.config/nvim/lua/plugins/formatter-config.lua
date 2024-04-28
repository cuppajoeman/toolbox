require('formatter').setup({
  logging = false,
  filetype = {
    --javascript = {
    --    -- prettier
    --   function()
    --      return {
    --        exe = "prettier",
    --        args = {"--stdin-filepath", vim.api.nvim_buf_get_name(0), '--single-quote'},
    --        stdin = true
    --      }
    --    end
    --},
    --rust = {
    --  -- Rustfmt
    --  function()
    --    return {
    --      exe = "rustfmt",
    --      args = {"--emit=stdout"},
    --      stdin = true
    --    }
    --  end
    --},
    python = {
        function()
          return {
            exe = "black",
            args = {"-q"},
            stdin = false
          }
        end
      }
  }
})
